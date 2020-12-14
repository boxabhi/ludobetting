import random
import requests
import json
# import paytmchecksum
import hashlib
import hmac
import base64
import string

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
        "appId" : '45107556fc3225a133718229d70154',
        "orderId" : orderId,
        "orderAmount" : orderAmount,
        "orderCurrency" : 'INR',
        "customerName" : 'Ludo betting',
        "customerPhone" : customerPhone,
        "customerEmail" : "abhijeetg40@gmail.com",
        "returnUrl" : 'http://127.0.0.1:800/0payment_success'
    }
    sortedKeys = sorted(postData)
    signatureData = ""
    for key in sortedKeys:
        signatureData += key+postData[key]
    print(signatureData)
    message = bytes(signatureData , 'utf-8')
    secret = bytes('a06a7684bc8aa6316763adad5ca60476160d48f7' , 'utf-8')
    signature = base64.b64encode(hmac.new(secret,message,digestmod=hashlib.sha256).digest()).decode("utf-8")
    return signature