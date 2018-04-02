import requests
import re
import json
api_details = json.load(open('./trainapi.json'))
regex = re.compile(api_details['seat_regex'])
url_template =  api_details['seat_endpt']
def seat_avail(train, src, dst,jclass,jdate, quota):
    # print(train,src,dst,jdate, jclass,quota)
    qry_url = url_template.replace('<train>',str(train)).replace('<src>',str(src).lower()).replace('<dst>',str(dst).lower()).replace('<jclass>',str(jclass).upper()).replace('<jdate>',str(jdate)).replace('<quota>',quota)
    # print(qry_url)
    res = requests.get(qry_url)
    if res.status_code != 200:
        print(res.status_code)
        return 'N/A'
    html = str(res.content)#.replace(' ','').replace('\t','').replace('\n','')
    matches = regex.findall(html)
    if matches is None or len(matches) == 0:
        print('no match')
        return 'N/A'
    return matches[0].split('>')[1].split('<')[0]
    # print(res.content)

# print(seat_avail('57625','kzj','mugr','SL','2018-03-31','GN'))