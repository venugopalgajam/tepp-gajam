import datetime as dt
import logging
from flask import Flask, redirect, render_template, request, url_for
from db_tools import connect_to, fetch_data, one_stop_query, direct_query, two_stops_query
from rendering_lib import render_table
from enquiry import seat_avail
import json
from fcm import send_push
import json
import enquiry

app = Flask(__name__)
CREDS_FILE = './mysqlvm-details.json'

@app.route('/enquiry')
def enquiry():
    return render_template('enquiry.html')

@app.route('/')
def index():
    return redirect(url_for('enquiry'))

@app.route('/service')
def get_service():
    return render_template('service.html')

@app.route('/register', methods=['POST'])
def get_registered():
    src = str(request.form['src']).split('-')[-1]
    dst = str(request.form['dst']).split('-')[-1]
    jdate = str(request.form['jdate'])
    sub_str = str(request.form['sub'])
    send_push(sub_str)
    return "hip hip hurray"

@app.route('/direct_trains')
def get_direct_trains():
    src = str(request.args['src']).split('-')[-1]
    dst = str(request.args['dst']).split('-')[-1]
    jdate = str(request.args['jdate'])
    db=connect_to(CREDS_FILE)
    with db.cursor() as cur:
        head, body = fetch_data(src,dst,jdate,direct_query,cur)
    db.close()
    body = list(body)
    body.insert(0, head)
    body.insert(0,1)
    return json.dumps(body, default=str)

@app.route('/one_stop')
def get_one_stop():
    src = str(request.args['src']).split('-')[-1]
    dst = str(request.args['dst']).split('-')[-1]
    jdate = str(request.args['jdate'])
    db=connect_to(CREDS_FILE)
    with db.cursor() as cur:
        head, body = fetch_data(src,dst,jdate,one_stop_query,cur)
    db.close()
    body = list(body)
    body.insert(0, head)
    body.insert(0,2)
    return json.dumps(body, default=str)

@app.route('/two_stops')
def get_two_stops():
    src = str(request.args['src']).split('-')[-1]
    dst = str(request.args['dst']).split('-')[-1]
    jdate = str(request.args['jdate'])
    db=connect_to(CREDS_FILE)
    with db.cursor() as cur:
        head, body = fetch_data(src,dst,jdate,two_stops_query,cur)
    db.close()
    body = list(body)
    body.insert(0, head)
    body.insert(0,3)
    return json.dumps(body, default=str)

@app.route('/seat_avail')
def get_seat_avail():
    data = json.loads(request.args['data'])[2:]
    print(data)
    id_ = request.args['id']
    cls_ = request.args['cls']
    quota = request.args['quota']
    jdate = request.args['jdate']
    # return json.dumps(data);
    return json.dumps([id_]+[seat_avail(i[0].split('-')[0], i[1].lower(), i[2].lower(), cls_.split('-')[1], jdate, quota.split('-')[1]) for i in data])

'''
@app.route('/get_paths',methods=['GET'])
def get_paths_html():
    db = connect_to(CREDS_FILE)
    src = str(request.args.get('src','')).split('-')[-1]
    dst = str(request.args.get('dst','')).split('-')[-1]
    date = str(request.args.get('jdate',''))
    responce_html =""
    head, body = fetch_data(src,dst,str(date),direct_query,db.cursor())
    responce_html=responce_html+ "<label>Direct Trains:</label>"+render_table("direct_tbl",head, body)
    head, body = fetch_data(src,dst,str(date),one_stop_query,db.cursor())
    responce_html=responce_html+"<label>One Stop Journey:</label>"+render_table("one_stop_tbl",head, body)
    return responce_html
'''

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

