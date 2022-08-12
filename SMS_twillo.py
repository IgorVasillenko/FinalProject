import os
from twilio.rest import Client

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
client = Client(account_sid, auth_token)


def sms_for_parents(phone_number, kid_id):
    body_message = f"{kid_id} is not in the institute"
    valid_phone_number = '+972' + phone_number[1:]
    msg = client.messages.create(
        from_='+19145064929',
        body=body_message,
        to=valid_phone_number
    )
    return msg
