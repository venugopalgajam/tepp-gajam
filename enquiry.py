import requests
import re
"""<divclass="seat_aval_result_left"id="first1">AVAILABLE-0003</div>"""
regex = re.compile(r"<div class=\"seat_aval_result_left\" id=\"first1\" >.*?</div>")
url_template = r"https://www.railyatri.in/seat-availability/<train>-<src>-<dst>?journey_class=<jclass>&journey_date=<jdate>&quota=<quota>"

def seat_avail(train, src, dst,jclass,jdate, quota):
    qry_url = url_template.replace('<train>',str(train)).replace('<src>',str(src).lower()).replace('<dst>',str(dst).lower()).replace('<jclass>',str(jclass).upper()).replace('<jdate>',str(jdate)).replace('<quota>',quota)
    # print(qry_url)
    res = requests.get(qry_url)
    if res.status_code != 200:
        print(res.status_code)
        return 'N/A'
    html = str(res.content)#.replace(' ','').replace('\t','').replace('\n','')
    matches = regex.findall(html)
    if matches is None or len(matches) == 0:
        return 'N/A'
    return matches[0].split('>')[1].split('<')[0]
    # print(res.content)

# print(seat_avail('57625','kzj','mugr','SL','2018-03-31','GN'))