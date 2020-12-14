import random
import requests


API_KEY = 'd959e6f9-32ea-11eb-83d4-0200cd936042'

def send_otp(mobile ):
    otp = random.randint(1000 , 9999)
    url = f'https://2factor.in/API/V1/{API_KEY}/SMS/{mobile}/{otp}'
    response = requests.get(url)
    return otp