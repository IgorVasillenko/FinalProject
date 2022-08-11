import os
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com / console
# account_sid = 'AC97edc83a2e341b01844d4d5e6a068a87'
# auth_token = 'f30b648c5ddb0d521383ca0edb0f8cbb'

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")

client = Client(account_sid, auth_token)


# message = client.messages.create(
#     from_='+19145064929',
#     body='205634967 is not in the institute',
#     to='+972525827107'
# )
#
# print(message.sid)


def sms_for_parents(phone_number, kid_id):
    body_message = f"{kid_id} is not in the institute"
    valid_phone_number = '+972' + phone_number[1:]
    client.messages.create(
        from_='+19145064929',
        body=body_message,
        to=valid_phone_number
    )

