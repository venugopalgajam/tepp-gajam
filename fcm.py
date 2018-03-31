from pywebpush import webpush
import json
def send_push(sub_str, data="registered!!"):
    sub = json.loads(sub_str)
    webpush(sub,data,vapid_private_key=json.load(open('./fcm-creds.json')),vapid_claims={"sub": "mailto:venugopalgajam@gmail.com"})