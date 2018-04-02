from pywebpush import webpush
import json
PRIVATE_KEY = json.load(open('./fcm-creds.json'))['private_key']
def send_push(sub_str, data="registered!!"):
    sub = json.loads(sub_str)
    webpush(sub,data,vapid_private_key=PRIVATE_KEY,vapid_claims={"sub": "mailto:venugopalgajam@gmail.com"})