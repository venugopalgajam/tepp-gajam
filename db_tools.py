"""
    mysql tools
"""
import os
import json
import MySQLdb

direct_query = """
select trno as Train_No, trnm as Train, src as Source, dt as Dept_Time, dst as Destination, at as Arr_Time from
(select 
trains.train_no as  trno,
trains.train_name as trnm,
hp1.stn_code as src,
hp2.stn_code as dst,
DATE("{{jdate}}") +INTERVAL to_seconds(hp1.dept_time)-to_seconds(DATE(now())) SECOND as dt,
DATE("{{jdate}}") +INTERVAL (hp2.sday-hp1.day)*24*60*60+to_seconds(hp2.arr_time)-to_seconds(DATE(now())) SECOND as at
from 
(select * from trains where {{jclass}}='1') as trains,
(select * from hops where hops.stn_code="{{src}}") as hp1,
(select * from hops where hops.stn_code="{{dst}}") as hp2
where 
hp1.train_no = trains.train_no and 
hp2.train_no = trains.train_no and 
hp1.hop_index < hp2.hop_index and
(trains.jday & (1 << (WEEKDAY(DATE("{{jdate}}")- INTERVAL (hp1.sday-1) DAY)))) > 0
) as tbl order by at,dt limit {{offset}},60;"""

one_stop_query= """select trno1 as Train1_No, trnm1 as Train1_Name, src1 as Source1,sdt1 as Dept_Time1, dst1 as Destination1, dat1 as Arr_Time1, SEC_TO_TIME(wt) as Waiting_Time ,trno2 as Train2_No,trnm2 as Train2_Name, src2 as Source2, sdt2 as Dept_Time2, dst2 as Destination2, dat2 as Arr_Time2
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
        (select * from trains where {{jclass}}='1') as tr1,
        (select * from hops where hops.stn_code = "{{src}}" ) as hp1,
        (select hops.train_no as train_no, hops.stn_code as stn_code, hops.arr_time as arr_time, hops.dept_time as dept_time , hops.hop_index as hop_index,hops.day as day, hops.sday as sday from hops,stations where hops.stn_code=stations.stn_code and stations.trains_cnt > 39) as hp2,
        (select * from trains where {{jclass}}='1') as tr2,
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
        (select * from trains where {{jclass}}='1') as tr1,
        (select * from hops where hops.stn_code = "{{src}}" ) as hp1,
        (select hops.train_no as train_no, hops.stn_code as stn_code, hops.arr_time as arr_time, hops.dept_time as dept_time , hops.hop_index as hop_index,hops.day as day, hops.sday as sday from hops,stations where hops.stn_code=stations.stn_code and stations.trains_cnt > 39) as hp2,
        (select * from trains where {{jclass}}='1') as tr2,
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
) as tbl where wt < 12*60*60  order by dat2,sdt1  limit {{offset}},60;
"""

two_stops_query = """"""
def connect_to(creds_file):
    db_creds = json.load(open(creds_file))
    return MySQLdb.connect(host=db_creds['host'], user=db_creds['user'], port= db_creds['port'], passwd=db_creds['passwd'],db=db_creds['db'])

def fetch_data(src,dst,jdate,jclass,qry_template,ptr,offset=0):
    if len(qry_template) <=0:
        return None, None
    qry = str(qry_template).replace('{{src}}',src).replace('{{dst}}',dst).replace('{{jdate}}',jdate).replace('{{offset}}',str(60*offset)).replace('{{jclass}}',jclass)
    #file =open('./op.txt','w');file.write(qry);file.close()
    ptr.execute(qry)
    columns = [tpl[0] for tpl in ptr.description]
    return columns,ptr.fetchall()
