"""
    mysql tools
"""
import os
import json
import MySQLdb

direct_query = """
select concat(trno,"<br>",trnm) as Train, concat(src,"<br>",dt) as "Source<br>Dept_Time", concat(dst,"<br>",at) as "Destination<br>Arr_Time" , concat("<span class=\\" avail ",trno,"_",src,"_",dst,"_",DATE(dt),"  \\">loading..</span> ") as SEAT_AVAIL from
(select 
trains.train_no as  trno,
trains.train_name as trnm,
hp1.stn_code as src,
hp2.stn_code as dst,
DATE("{{jdate}}") +INTERVAL to_seconds(hp1.dept_time)-to_seconds(DATE(now())) SECOND as dt,
DATE("{{jdate}}") +INTERVAL (hp2.sday-hp1.day)*24*60*60+to_seconds(hp2.arr_time)-to_seconds(DATE(now())) SECOND as at
from 
trains,
(select * from hops where hops.stn_code="{{src}}") as hp1,
(select * from hops where hops.stn_code="{{dst}}") as hp2
where 
hp1.train_no = trains.train_no and 
hp2.train_no = trains.train_no and 
hp1.hop_index < hp2.hop_index and
(trains.jday & (1 << (WEEKDAY(DATE("{{jdate}}")- INTERVAL (hp1.sday-1) DAY)))) > 0
) as tbl order by at;"""

one_stop_query= """select concat(trno1,"<br>",trnm1) as Train1, concat(src1,'<br>',sdt1) as "Source <br> Dept_Time", concat(dst1,'<br>',dat1) as "Destination <br> Arr_Time",concat("<span class=\\" avail ",trno1,"_",src1,"_",dst1,"_",DATE(sdt1),"\\" >loading..</span> ")  as "SEAT_AVAIL", SEC_TO_TIME(wt) as "Waiting Time", concat(trno2,"<br>",trnm2) as Train2 , concat(src2,'<br>',sdt2) as "Source<br> Dept_Time", concat(dst2,'<br>',dat2) as "Destination<br> Arr_Time",concat("<span class=\\" avail ",trno2,"_",src2,"_",dst2,"_",DATE(sdt2),"\\" >loading..</span> ")  as "SEAT_AVIBL"
from
(
    select tr1.train_no as trno1,
    tr1.train_name trnm1,
    hp1.stn_code "src1",
    hp2.stn_code "dst1",
    (DATE("{{jdate}}") + INTERVAL (TO_SECONDS(hp1.dept_time)-to_seconds(DATE(NOW()))) SECOND) "sdt1",
    (DATE("{{jdate}}")+  INTERVAL ((hp2.sday-hp1.day)*24*60*60 + TO_SECONDS(hp2.arr_time)-to_seconds(DATE(NOW()))) SECOND) "dat1",
    ( to_seconds(hp3.dept_time)-to_seconds(hp2.arr_time) ) as "wt", 
    tr2.train_no trno2,
    tr2.train_name trnm2,
    hp2.stn_code "src2",
    hp4.stn_code "dst2",
    (DATE("{{jdate}}") + INTERVAL ((hp2.sday-hp1.day)*24*60*60 + TO_SECONDS(hp3.dept_time)-to_seconds(DATE(NOW()))) SECOND) "sdt2",
    (DATE("{{jdate}}") + INTERVAL ((hp2.sday-hp1.day+hp4.sday-hp3.day)*24*60*60 + TO_SECONDS(hp4.arr_time)-to_seconds(DATE(NOW()))) SECOND) "dat2"
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

    select tr1.train_no trno1,
    tr1.train_name trnm1,
    hp1.stn_code "src1",
    hp2.stn_code "dst1",
    (DATE("{{jdate}}") + INTERVAL (TO_SECONDS(hp1.dept_time)-to_seconds(DATE(NOW()))) SECOND) "sdt1",
    (DATE("{{jdate}}")+  INTERVAL ((hp2.sday-hp1.day)*24*60*60 + TO_SECONDS(hp2.arr_time)-to_seconds(DATE(NOW()))) SECOND) "dat1",
    (TO_SECONDS(hp3.dept_time)-to_seconds(hp2.arr_time) + 24*60*60) AS "wt",
    tr2.train_no as trno2,
    tr2.train_name as  trnm2,
    hp2.stn_code "src2",
    hp4.stn_code "dst2",
    (DATE("{{jdate}}") + INTERVAL ((hp2.sday-hp1.day+1)*24*60*60 + TO_SECONDS(hp3.dept_time)-to_seconds(DATE(NOW()))) SECOND) "sdt2",
    (DATE("{{jdate}}") + INTERVAL ((hp2.sday-hp1.day+1+hp4.sday-hp3.day)*24*60*60 + TO_SECONDS(hp4.arr_time)-to_seconds(DATE(NOW()))) SECOND) "dat2"
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
) as tbl where wt < 12*60*60  order by dat2,wt  limit 60;
"""

two_stops_query = """"""
def connect_to(creds_file):
    db_creds = json.load(open(creds_file))
    return MySQLdb.connect(host=db_creds['host'], user=db_creds['user'], port= db_creds['port'], passwd=db_creds['passwd'],db=db_creds['db'])

def fetch_data(src,dst,jdate,qry,ptr):
    if len(qry) <=0:
        return None, None
    one_stop_qry = str(qry).replace('{{src}}',src).replace('{{dst}}',dst).replace('{{jdate}}',jdate)
    file =open('./op.txt','w')
    file.write(one_stop_qry)
    file.close()
    with open('op.txt','w') as file:
        file.write(one_stop_qry)
    ptr.execute(one_stop_qry)
    columns = [ tpl[0] for tpl in ptr.description]
    return columns,ptr.fetchall()
