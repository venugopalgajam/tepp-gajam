"""
    mysql tools
"""
import os
import json
import MySQLdb

direct_query = """select 
concat(trains.train_no,"-",trains.train_name) as Train,
hp1.stn_code as "Source Station",
hp2.stn_code as "Destination Station",
DATE("{{jdate}}") +INTERVAL to_seconds(hp1.dept_time)-to_seconds(DATE(now())) SECOND as Dept,
DATE("{{jdate}}") +INTERVAL (hp2.sday-hp1.day)*24*60*60+to_seconds(hp2.arr_time)-to_seconds(DATE(now())) SECOND as Arr,
"N/A" as Seat_AVAIL
from 
trains,
(select * from hops where hops.stn_code="{{src}}") as hp1,
(select * from hops where hops.stn_code="{{dst}}") as hp2
where 
hp1.train_no = trains.train_no and 
hp2.train_no = trains.train_no and 
hp1.hop_index < hp2.hop_index and
(trains.jday & (1 << (WEEKDAY(DATE("{{jdate}}")- INTERVAL (hp1.sday-1) DAY)))) > 0"""

one_stop_query= """select *, "N/A" as "Train1 SEAT_AVAIL", "N/A" AS "Train2 Seat_AVAIL"
from
(
    select concat(tr1.train_no,"-",tr1.train_name) Train1,
    concat(tr2.train_no,"-",tr2.train_name) Train2,
    hp1.stn_code "Source Station",
    hp2.stn_code "Intermediate Station",
    hp4.stn_code "Destination Station",
    (DATE("{{jdate}}") + INTERVAL (TO_SECONDS(hp1.dept_time)-to_seconds(DATE(NOW()))) SECOND) "Source Dept. Time",
    (DATE("{{jdate}}")+  INTERVAL ((hp2.sday-hp1.day)*24*60*60 + TO_SECONDS(hp2.arr_time)-to_seconds(DATE(NOW()))) SECOND) "Intermediate Arr. Time",
    (DATE("{{jdate}}") + INTERVAL ((hp2.sday-hp1.day)*24*60*60 + TO_SECONDS(hp3.dept_time)-to_seconds(DATE(NOW()))) SECOND) "Intermediate Dept. Time",
    (DATE("{{jdate}}") + INTERVAL ((hp2.sday-hp1.day+hp4.sday-hp3.day)*24*60*60 + TO_SECONDS(hp4.arr_time)-to_seconds(DATE(NOW()))) SECOND) "Destination Arr. Time"
    from 
        trains as tr1,
        (select * from hops where hops.stn_code = "{{src}}" ) as hp1,
        (select hops.train_no as train_no, hops.stn_code as stn_code, hops.arr_time as arr_time, hops.dept_time as dept_time , hops.hop_index as hop_index,hops.day as day, hops.sday as sday from hops,stations where hops.stn_code=stations.stn_code and stations.trains_cnt > 39) as hp2,
        trains as tr2,
        (select hops.train_no as train_no, hops.stn_code as stn_code, hops.arr_time as arr_time, hops.dept_time as dept_time , hops.hop_index as hop_index,hops.day as day, hops.sday as sday from hops,stations where hops.stn_code=stations.stn_code and stations.trains_cnt > 39) as hp3,
        (select * from hops where hops.stn_code= "{{dst}}" ) as hp4 
    where
    tr1.train_no = hp1.train_no and
    hp1.train_no = hp2.train_no and 
    hp1.hop_index < hp2.hop_index and
    tr2.train_no = hp3.train_no and
    hp3.train_no = hp4.train_no and  
    hp3.hop_index < hp4.hop_index and 
    hp2.stn_code = hp3.stn_code and
    tr1.train_no <> tr2.train_no and
    (tr1.jday & (1 << (WEEKDAY(DATE("{{jdate}}")- INTERVAL (hp1.sday-1) DAY)))) > 0 and
    (tr2.jday & (1 << (WEEKDAY(DATE("{{jdate}}") + INTERVAL hp2.sday-hp1.day DAY)))) > 0 and 
    hp2.arr_time < hp3.dept_time
    union
    select concat(tr1.train_no,"-",tr1.train_name) Train1,
    concat(tr2.train_no,"-",tr2.train_name) Train2,
    hp1.stn_code "Source Station",
    hp2.stn_code "Intermediate Station",
    hp4.stn_code "Destination Station",
    (DATE("{{jdate}}") + INTERVAL (TO_SECONDS(hp1.dept_time)-to_seconds(DATE(NOW()))) SECOND) "Source Dept. Time",
    (DATE("{{jdate}}")+  INTERVAL ((hp2.sday-hp1.day)*24*60*60 + TO_SECONDS(hp2.arr_time)-to_seconds(DATE(NOW()))) SECOND) "Intermediate Arr. Time",
    (DATE("{{jdate}}") + INTERVAL ((hp2.sday-hp1.day+1)*24*60*60 + TO_SECONDS(hp3.dept_time)-to_seconds(DATE(NOW()))) SECOND) "Intermediate Dept. Time",
    (DATE("{{jdate}}") + INTERVAL ((hp2.sday-hp1.day+1+hp4.sday-hp3.day)*24*60*60 + TO_SECONDS(hp4.arr_time)-to_seconds(DATE(NOW()))) SECOND) "Destination Arr. Time"
    from 
        trains as tr1,
        (select * from hops where hops.stn_code = "{{src}}" ) as hp1,
        (select hops.train_no as train_no, hops.stn_code as stn_code, hops.arr_time as arr_time, hops.dept_time as dept_time , hops.hop_index as hop_index,hops.day as day, hops.sday as sday from hops,stations where hops.stn_code=stations.stn_code and stations.trains_cnt > 39) as hp2,
        trains as tr2,
        (select hops.train_no as train_no, hops.stn_code as stn_code, hops.arr_time as arr_time, hops.dept_time as dept_time , hops.hop_index as hop_index,hops.day as day, hops.sday as sday from hops,stations where hops.stn_code=stations.stn_code and stations.trains_cnt > 39) as hp3,
        (select * from hops where hops.stn_code= "{{dst}}") as hp4 
    where
    tr1.train_no = hp1.train_no and
    hp1.train_no = hp2.train_no and 
    hp1.hop_index < hp2.hop_index and
    tr2.train_no = hp3.train_no and
    hp3.train_no = hp4.train_no and  
    hp3.hop_index < hp4.hop_index and 
    hp2.stn_code = hp3.stn_code  and
    tr1.train_no <> tr2.train_no and
    (tr1.jday & (1 << (WEEKDAY("{{jdate}}"- INTERVAL (hp1.sday-1) DAY)))) > 0 and
    (tr2.jday & (1 << WEEKDAY("{{jdate}}" + INTERVAL hp2.sday-hp1.day+1 DAY))) > 0
) as hip order by "Destination Arr. Time" limit 60;
"""

two_stops_query = """"""
def connect_to(creds_file):
    db_creds = json.load(open(creds_file))
    return MySQLdb.connect(host=db_creds['host'], user=db_creds['user'], port= db_creds['port'], passwd=db_creds['passwd'],db=db_creds['db'])

def fetch_data(src,dst,jdate,qry,ptr):
    if len(qry) <=0:
        return None, None
    one_stop_qry = str(qry).replace('{{src}}',src).replace('{{dst}}',dst).replace('{{jdate}}',jdate)
    with open('op.txt','w') as file:
        file.write(one_stop_qry)
    ptr.execute(one_stop_qry)
    columns = [ tpl[0] for tpl in ptr.description]
    return columns,ptr.fetchall()
