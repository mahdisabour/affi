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
    url = "https://console.melipayamak.com/api/send/shared/ab7e45a6a3cf48d7b60939dbcae698ce"
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