import random
import requests
import json
# import paytmchecksum
import hashlib
import hmac
import base64
import string
from django.conf import settings

MID= 'iopJfM06937972893222'
KEY = '#F9e%toAivZgqt1d'

# def check_payment_status(orderId , amount):
#     paytmParams = dict()
#     paytmParams["body"] = {
#     "mid" : MID,
#     "orderId" : orderId,
#     }
#     checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]), KEY)
#     paytmParams["head"] = {
#     "signature"	: checksum
#     }
#     post_data = json.dumps(paytmParams)

#     url = "https://securegw.paytm.in/v3/order/status"
#     response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
#     return response


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def make_payment(orderId , orderAmount, customerName ,customerPhone , returnUrl):
    postData = {
        "appId" : settings.APP_ID,
        "orderId" : orderId,
        "orderAmount" : orderAmount,
        "orderCurrency" : 'INR',
        "customerName" : 'Ludo betting',
        "customerPhone" : customerPhone,
        "customerEmail" : "abhijeetg40@gmail.com",
        "returnUrl" : settings.RETURN_URL
    }
    sortedKeys = sorted(postData)
    signatureData = ""
    for key in sortedKeys:
        signatureData += key+postData[key]
    print(signatureData)
    message = bytes(signatureData , 'utf-8')
    secret = bytes(settings.APP_SECRET , 'utf-8')
    signature = base64.b64encode(hmac.new(secret,message,digestmod=hashlib.sha256).digest()).decode("utf-8")
    return signature