import jwt
import json
import requests
from tmlib.settings import Settings
from connexion import NoContent, request
from tmlib.models import WPJWT, Customer, Minion, License, Registration
from datetime import datetime, timedelta
from tmlib.tm_obfuscate import deobfuscate, obfuscate
import logging


class Events:

    wp_url = f"{Settings.WP_HOST}/wp-json/"

    logger = logging.getLogger()

    def get_event(self, event_name: str) -> callable:
        """
        Entry point of the class
        Return a function to treat filled action
        """
        return getattr(self, event_name.replace("-", "_"))

    # Hooks
    def member_signup_completed(self, data):
        """
        When a user joins the site, they get added to the WordPress user DB. 
        This trigger should add them as a Customer (Set-Customer) through the web service.
        Fields:
        Login (email), Givenname/firstname, surname
        """
        try:
            member_id = data.get("id")
            member_data = self._get_member_data(member_id)
            customer = Customer(
                login=member_data["email"],
                given_name=member_data["first_name"],
                surname=member_data["last_name"],
            )
            customer.save()
        except Exception as e:
            self.logger.warning(e)

    def subscription_created(self, data):
        """
        Customers subscribe to Trading Minions product licenses. 
        MemberPress uses a combination of ‘Memberships’, ‘Transactions’ and ‘Subscription’ 
        to record the ‘active’ and expiry information of these. 
        Each product licence edition e.g. Clipper Gold, Silver etc has a corresponding 
        Memberpress ‘MembershipID’ (need to check this, I think the JSON refers to this 
        as a subscription id – incorrectly)
        When they sign up to a membership, a Transaction is created with an expiry. 
        This trigger and information should update/create the corresponding licence in mongodb
        Fields
        Transation (membershipID -> mongodb: customer/license/subscriptionid)
        Transaction expiry -> customer/license/support_expires
        """

        def create_or_update_registration(
            license_obj: License,
            account_number: int,
            broker_name: str,
            expiration_date: str,
            max_lots: int = 5,
            is_demo_account: bool = False,
        ) -> License:
            """
            Helper for the registration
            """
            r: Registration
            for r in license_obj.account_registrations:
                # if registration exists -> update rego_key
                if (
                    str(r.account_number).strip() == str(account_number).strip()
                    and str(r.broker).strip() == str(broker_name).strip()
                ):
                    r.rego_key = obfuscate(f"{account_number}--{expiration_date}")
                    r.maximum_lots = max_lots
                    break
            else:
                # if doesn't add a new registration object
                license_obj.account_registrations.append(
                    Registration(
                        account_number=account_number,
                        broker=broker_name,
                        rego_key=obfuscate(f"{account_number}--{expiration_date}"),
                        maximum_lots=max_lots,
                        is_demo_account=is_demo_account,
                    )
                )
            return license_obj

        subscription_id = data.get("id")
        subscription_data = self._get_subscription_id(subscription_id)

        member_id = data.get("member").get("id")
        member_data = self._get_member_data(member_id)

        minion_name, minion_edition = self._get_minions_data(subscription_data)
        # get broker name from the API
        broker_name = self._get_broker_by_value(
            member_data["profile"]["mepr_broker_name"]
        )
        self.logger.info(f"broker_name: {broker_name}")
        account_number = member_data["profile"]["mepr_broker_account_for_registration"]

        created_date = datetime.strptime(
            subscription_data.get("created_at"), "%Y-%m-%d %H:%M:%S"
        )
        expiration_date = created_date.replace(year=created_date.year + 1)
        expiration_date = datetime.strftime(expiration_date, "%Y.%m.%d")
        membership_id = subscription_data["membership"]["id"]
        self.logger.info(
            f"{minion_name}, {minion_edition}, {broker_name}, {expiration_date}"
        )
        customer: Customer = Customer.objects.get(login=member_data["email"])
        license_obj: License = customer.get_license(minion_name)
        if license_obj is None:
            # create
            self.logger.info("Create license")
            license_obj = License(
                minion_name=minion_name,
                wp_membership_id=membership_id,
                support_expires=expiration_date,
                minion_license=[],
            )
            customer.licenses.append(license_obj)
        else:
            # update license
            license_obj.wp_membership_id = membership_id
            license_obj.minion_license = minion_edition
            license_obj.support_expires = expiration_date
        # registration
        license_obj: License = create_or_update_registration(
            license_obj=license_obj,
            account_number=account_number,
            broker_name=broker_name,
            expiration_date=expiration_date,
        )
        # get maximum lots from the WP
        maximum_lots = self._get_max_lot_by_minion(
            minion_name=minion_name, minion_edition=minion_edition
        )
        registrations_count = len(license_obj.account_registrations)
        if registrations_count:
            maximum_lots_per_registration = maximum_lots / registrations_count
            r: Registration
            for r in license_obj.account_registrations:
                r.maximum_lots = maximum_lots_per_registration
        license_obj.save()
        customer.save()

    def member_account_updated(self, data):
        """
        Any change to their details in Wordpress should trigger a corresponding update in mongoDB
        Login (email), Givenname/firstname, surname
        Also: custom fields Broker name, Broker account
        (need some better field names here to associate them with a single product e.g. Clipper)
        So
        Custom field
        WP: User.ClipperBrokerName -> mongodb: customer/license[Clipper]/broker_name
        WP: User.ClipperAccountNumber -> mongodb: customer/license[Clipper]/account_number
        Note: A newAccount setup will also require a call to Set-RegoKey 
        to generate a registration key.
        """
        try:
            signup_id = data.get("id")
            member_data = self._get_member_data(signup_id)
            customer = Customer.objects.get(login=member_data["email"])
            customer.given_name = member_data["first_name"]
            customer.surname = member_data["last_name"]
            customer.save()
            # TODO: Add logic to change broker name/ broker id
        except Exception as e:
            self.logger.warning(e)

    def subscription_paused(self, data):
        """
        This prevents the product from operating.
        Set support expires
        """
        subscription_id = data.get("id")
        subscription_data = self._get_subscription_id(subscription_id)
        customer_login = subscription_data["member"]["email"]
        minion_name, minion_edition = self._get_minions_data(subscription_data)
        customer: Customer = Customer.objects.get(login=customer_login)

        clicense: License
        for clicense in customer.licenses:
            if (
                clicense.minion_name.strip() == minion_name
                and clicense.minion_license.strip() == minion_edition
            ):
                clicense.support_expires = datetime.now().strftime("%Y.%m.%d")
                self.logger.info(clicense)
                clicense.save()

    def subscription_stopped(self, data):
        """
        This prevents the product from operating.
        Set support expires
        """
        subscription_id = data.get("id")
        subscription_data = self._get_subscription_id(subscription_id)
        customer_login = subscription_data["member"]["email"]
        minion_name, minion_edition = self._get_minions_data(subscription_data)
        customer: Customer = Customer.objects.get(login=customer_login)

        clicense: License
        for clicense in customer.licenses:
            if (
                clicense.minion_name.strip() == minion_name
                and clicense.minion_license.strip() == minion_edition
            ):
                clicense.support_expires = datetime.now().strftime("%Y.%m.%d")
                self.logger.info(clicense)
                clicense.save()

    def subscription_upgraded(self, data):
        """
        Each Clipper edition has a different maximum_lots. 
        If the user upgrades (or downgrades), then the maximum_lots needs to change.
        Note. The subscription is for a the maximum_lots to apply over all accounts.
        So if a customer had 2 accounts, then maximum_lots = 5.0 would 
        mean that the sum of maximum_lots for both accounts must not add up to more than 5.0.
        Need to think about some way to allow end users to allocate this. 
        Maybe additional custom fields in WP.
        """
        subscription_id = data.get("id")
        subscription_data = self._get_subscription_id(subscription_id)
        customer_login = subscription_data["member"]["email"]
        minion_name, minion_edition = self._get_minions_data(subscription_data)
        customer: Customer = Customer.objects.get(login=customer_login)

        created_date = datetime.strptime(
            subscription_data.get("created_at"), "%Y-%m-%d %H:%M:%S"
        )
        expiration_date = created_date.replace(year=created_date.year + 1)
        expiration_date = datetime.strftime(expiration_date, "%Y.%m.%d")

        maximum_lots = self._get_max_lot_by_minion(
            minion_name=minion_name, minion_edition=minion_edition
        )

        clicense: License
        for clicense in customer.licenses:
            if clicense.minion_name.strip() == minion_name:
                clicense.support_expires = expiration_date
                clicense.minion_license = minion_edition
                registrations_count = len(clicense.account_registrations)
                if registrations_count:
                    max_lots_per_reg = maximum_lots / registrations_count
                    for cregistration in clicense.account_registrations:
                        cregistration.max_lots = max_lots_per_reg
                clicense.save()

    def subscription_downgraded(self, data):
        """
        TODO: test me
        See above
        """
        subscription_id = data.get("id")
        subscription_data = self._get_subscription_id(subscription_id)
        customer_login = subscription_data["member"]["email"]
        minion_name, minion_edition = self._get_minions_data(subscription_data)
        customer: Customer = Customer.objects.get(login=customer_login)

        created_date = datetime.strptime(
            subscription_data.get("created_at"), "%Y-%m-%d %H:%M:%S"
        )
        expiration_date = created_date.replace(year=created_date.year + 1)
        expiration_date = datetime.strftime(expiration_date, "%Y.%m.%d")

        maximum_lots = self._get_max_lot_by_minion(
            minion_name=minion_name, minion_edition=minion_edition
        )

        clicense: License
        for clicense in customer.licenses:
            if clicense.minion_name.strip() == minion_name:
                clicense.support_expires = expiration_date
                clicense.minion_license = minion_edition
                registrations_count = len(clicense.account_registrations)
                if registrations_count:
                    max_lots_per_reg = maximum_lots / registrations_count
                    for cregistration in clicense.account_registrations:
                        cregistration.max_lots = max_lots_per_reg
                clicense.save()

    def subscription_expired(self, data):
        """
        See above
        """
        subscription_id = data.get("id")
        subscription_data = self._get_subscription_id(subscription_id)
        customer_login = subscription_data["member"]["email"]
        minion_name, minion_edition = self._get_minions_data(subscription_data)
        customer: Customer = Customer.objects.get(login=customer_login)

        clicense: License
        for clicense in customer.licenses:
            if (
                clicense.minion_name.strip() == minion_name
                and clicense.minion_license.strip() == minion_edition
            ):
                clicense.support_expires = datetime.now().strftime("%Y.%m.%d")
                self.logger.info(clicense)
                clicense.save()

    # eof Hooks
    def _get_max_lot_by_minion(self, minion_name, minion_edition):
        needle = f"{minion_name}: {minion_edition}"
        for element in self._get_max_lots():
            if element["minion"] == needle:
                return float(element["max_lots"])
        return 0

    def _get_max_lots(self):
        return self._execute_request(f"tm-conf/v1/max-lots")

    def _get_broker_by_value(self, broker_value):
        for element in self._get_brokers():
            if element["broker_value"] == broker_value:
                return element["broker_name"]
        return None

    def _get_brokers(self):
        return self._execute_request(f"tm-conf/v1/brokers")

    def _get_minions_data(self, subscription_data):
        try:
            subscription_title = subscription_data["membership"]["title"]
            minion_name, minion_edition = subscription_title.split(":")
            return minion_name.strip(), minion_edition.strip()
        except:
            self.logger.error(
                f"Transaction with id {subscription_data['id']}"
                f"has a membership {subscription_data['membership']['id']} (title: '{title}')"
            )
            return None, None

    def _get_member_data(self, member_id):
        return self._execute_request(f"mp/v1/members/{member_id}")

    def _get_subscription_id(self, subscription_id):
        return self._execute_request(f"mp/v1/subscriptions/{subscription_id}")

    def _request_auth_token(self):
        url = f"{self.wp_url}jwt-auth/v1/token"
        response = requests.request(
            "POST",
            url,
            data={"username": Settings.WP_USER, "password": Settings.WP_PASSWORD},
        )
        reponse_json = response.json()
        return reponse_json.get("token")

    def _execute_request(self, url_suffix):
        token: str = self._get_auth_token()
        url = self.wp_url + url_suffix
        self.logger.info(url)
        response = requests.get(url, headers={"Authorization": "Bearer " + token})
        return response.json()

    def _get_auth_token(self):
        token = WPJWT.objects(username=Settings.WP_USER).first()
        try:
            self.logger.info("get_auth_token")
            self.logger.info(token.token)
            jwt.decode(token.token.encode("utf-8"), Settings.WP_JWT_SECRET)
            token_string = token.token
            self.logger.info("token from db")
        except Exception as e:
            self.logger.warning(e)
            token_string = self._request_auth_token()
            WPJWT.objects(username=Settings.WP_USER).update_one(
                set__token=token_string, upsert=True
            )
        return token_string


allowed_events = {
    "member-signup-completed",
    "subscription-created",
    "member-account-updated",
    "subscription-paused",
    "subscription-stopped",
    "subscription-upgraded",
    "subscription-downgraded",
    "subscription-expired",
}


def trigger():
    logger = logging.getLogger()
    logger.info("trigger")
    hook_data = json.loads(request.data)
    event: str = hook_data["event"]
    if event not in allowed_events:
        return NoContent, 422
    event_data = hook_data["data"]
    Events().get_event(event)(event_data)

    return NoContent, 200
