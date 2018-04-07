import datetime as dt
import json
import logging
from threading import Thread
import time

from flask import Flask, redirect, render_template, request, url_for

from db_tools import connect_to, direct_query, fetch_data, one_stop_query,two_stops_query
from rendering_lib import render_table
from utils import seat_avail, send_push, curravail_thread

app = Flask(__name__)
CREDS_FILE = './mysqlvm-details.json'

# if __name__ == "__main__":
#     # Setting debug to True enables debug output. This line should be
#     # removed before deploying a production app.
#     app.debug = True
#     app.run()

@app.route('/enquiry')
def enquiry():
    return render_template('enquiry.html')

@app.route('/')
def index():
    return redirect(url_for('enquiry'))

@app.route('/seatavail')
def get_seat_avail():
    jtrain = str(request.args['jtrain'])
    jsrc = str(request.args['jsrc']).lower()
    jdst = str(request.args['jdst']).lower()
    jclass = str(request.args['jclass']).split('-')[-1]
    jdate = str(request.args['jdate'])
    quota = str(request.args['quota']).split('-')[-1]
    res = dict()
    res['id'] = r".{0}_{1}_{2}_{3}".format(jtrain,jsrc.upper(),jdst.upper(),jdate)
    res['avail'] = seat_avail(jtrain,jsrc,jdst,jclass,jdate,quota)
    #print(res)
    return json.dumps(res)

@app.route('/service')
def get_service():
    return render_template('service.html')

@app.route('/register', methods=['POST'])
def get_registered():
    print(request.form)
    src = str(request.form['src']).split('-')[-1]
    dst = str(request.form['dst']).split('-')[-1]
    jdate = str(request.form['jdate'])
    jclass = str(request.form['jclass'])
    sub_str = str(request.form['sub'])
    quota = str(request.form['quota'])
    cur_date = int(float(request.form['cur_date']))
    db=connect_to(CREDS_FILE)
    with db.cursor() as cur:
        head, body = fetch_data(src,dst,jdate,jclass,direct_query,cur)
    db.close()
    trn_idx = list(head).index('Train_No')
    dt_idx = list(head).index('Dept_Time')
    trains = [row[trn_idx] for row in body]
    max_timestamp = max([time.mktime(row[dt_idx].timetuple()) for row in body])
    check_cnt = (1 if ((max_timestamp-cur_date)%(900)) > 0 else 0) + (max_timestamp-cur_date)//(900)
    Thread(target=curravail_thread,args=(list(trains),src,dst,jclass,quota,jdate,check_cnt,sub_str)).start()
    send_push(sub_str,"trains checked"+",".join(trains))
    return "Registered Successfully!!"

@app.route('/direct_trains')
def get_direct_trains():
    src = str(request.args['src']).split('-')[-1]
    dst = str(request.args['dst']).split('-')[-1]
    jdate = str(request.args['jdate'])
    jclass = str(request.args['jclass'])
    offset = str(request.args['offset'])
    db=connect_to(CREDS_FILE)
    with db.cursor() as cur:
        head, body = fetch_data(src,dst,jdate,jclass,direct_query,cur,offset)
    db.close()
    response = {}
    response['head'] = head
    response['body'] = body
    response['type'] = 1
    return json.dumps(response, default=str)

@app.route('/one_stop')
def get_one_stop():
    src = str(request.args['src']).split('-')[-1]
    dst = str(request.args['dst']).split('-')[-1]
    jdate = str(request.args['jdate'])
    jclass = str(request.args['jclass'])
    offset = str(request.args['offset'])
    db=connect_to(CREDS_FILE)
    with db.cursor() as cur:
        head, body = fetch_data(src,dst,jdate,jclass,one_stop_query,cur, offset)
    db.close()
    response = {}
    response['head'] = head
    response['body'] = body
    response['type'] = 2
    return json.dumps(response, default=str)

@app.route('/two_stops')
def get_two_stops():
    src = str(request.args['src']).split('-')[-1]
    dst = str(request.args['dst']).split('-')[-1]
    jdate = str(request.args['jdate'])
    jclass = str(request.args['jclass'])
    offset = str(request.args['offset'])
    db=connect_to(CREDS_FILE)
    with db.cursor() as cur:
        head, body = fetch_data(src,dst,jdate,jclass,two_stops_query,cur,offset)
    db.close()
    response = {}
    response['head'] = head
    response['body'] = body
    response['type'] = 3
    return json.dumps(response, default=str)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
