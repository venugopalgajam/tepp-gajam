import json
import re
import time

import requests

from pywebpush import webpush

PRIVATE_KEY = json.load(open('./fcm-creds.json'))['private_key']
def send_push(sub_str, data="registered!!"):
    sub = json.loads(sub_str)
    webpush(sub,data,vapid_private_key=PRIVATE_KEY,vapid_claims={"sub": "mailto:venugopalgajam@gmail.com"})

api_details = json.load(open('./trainapi.json'))
regex = re.compile(api_details['seat_regex'])
url_template =  api_details['seat_endpt']
def seat_avail(train, src, dst,jclass,jdate, quota):
    # print(train,src,dst,jdate, jclass,quota)
    qry_url = url_template.replace('<train>',str(train).strip()).replace('<src>',str(src).lower().strip()).replace('<dst>',str(dst).lower().strip()).replace('<jclass>',str(jclass).upper().strip()).replace('<jdate>',str(jdate).strip()).replace('<quota>',str(quota).upper().strip())
    # print(qry_url)
    trails = 4
    while trails > 0:
        trails -=1
        
        res = requests.get(qry_url)
        if res.status_code != 200:
            print(res.status_code)
            continue
        html = str(res.content)#.replace(' ','').replace('\t','').replace('\n','')
        matches = regex.findall(html)
        
        if matches is None or len(matches) == 0:
            print('no match',qry_url)
            continue
        return matches[0].split('>')[1].split('<')[0]
    return "N/A"
    # print(res.content)

# print(seat_avail('57625','kzj','mugr','SL','2018-03-31','GN'))

def curravail_thread(trains,src,dst,jclass,quota,jdate,check_cnt,sub_str):
    print(trains,src,dst,jclass,quota,jdate,check_cnt,sub_str)
    data = dict()
    data['src']=src
    data['dst']=dst
    data['jclass']=jclass
    data['quota']=quota
    while check_cnt > 0 and len(trains) > 0:
        for train in trains:
            res_str = seat_avail(train,src,dst,jclass,jdate,quota).strip()
            if res_str.startswith('CURR'):
                data['train']=train
                data['avail']=res_str
                return send_push(sub_str,json.dumps(data))
            elif res_str.startswith('TRAIN DEPARTED'):
                trains.remove(train)
        time.sleep(15*60)
        check_cnt -=1
    
    for train in trains:
        res_str = seat_avail(train,src,dst,jclass,jdate,quota)
        if res_str.startswith('CURR'):
            data['train']=train
            data['avail']=res_str
            return send_push(sub_str,json.dumps(data))
        elif res_str.startswith('TRAIN DEPARTED'):
            trains.remove(train)
    data['train']="N/A"
    data['avail']="Sorry!!"
    return send_push(sub_str,json)