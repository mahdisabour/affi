import requests

from ..celery import app
from .models import OTP

@app.task
def disableOTP(*args):
    instance = OTP.objects.get(id = args[0])
    instance.is_valid = False
    instance.save()


@app.task
def send_sms(phone_number, msg):
    url = "https://console.melipayamak.com/api/send/shared/8f892b16c22a4b3f89072fb00ee45cb6"
    bodyId = 62753
    args = [str(phone_number), str(msg)]
    print(url)
    print(phone_number, "->", msg)

    body = { 
    "bodyId": bodyId, 
    "to": str(phone_number), 
    "args": args
    }
    r = requests.post(url, json=body)
    print(r.text)
    print(r.status_code)