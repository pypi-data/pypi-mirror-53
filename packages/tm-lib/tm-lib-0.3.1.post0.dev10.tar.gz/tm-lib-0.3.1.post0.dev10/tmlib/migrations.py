from datetime import datetime
from tmlib.models import Customer


def migrate():
    for customer in Customer.objects():
        for licence in customer.licenses:
            for registration in licence.account_registrations:
                for checkin in registration.checkins:
                    if checkin.terminal_path is None:
                        checkin.terminal_path = 'NO_TERMINAL_PATH'
                        checkin.save()
