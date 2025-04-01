import socket
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for, session, make_response
import json
import os
import threading
from project_function import *
app = Flask(__name__)
app.secret_key = 'super secret key'
pri_data = ""
pri_category =""
sec_data = ""
sec_category =""
admin_list= {}
user_list= {}
def ipadd():
    hostname=socket.gethostname()
    IPAddr=socket.gethostbyname(hostname)
    return IPAddr
@app.route('/', methods=['POST', 'GET'])
def check_out():
    global random_id
    admin_list = get_key_value(showData("/Admin"))
    user_list = get_key_value(showData("/User"))
    error = None
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        if check_pass(account, password, admin_list):
            random_id = generate_random_string(40)
            session['logged_in'] = True
            session['accessed_dashboard'] = True
            return redirect(url_for('final_check', account= 'admin', random_pin= random_id))
        elif check_pass(account, password, user_list):
            random_id = generate_random_string(40)
            session['logged_in'] = True
            session['accessed_dashboard'] = True
            return redirect(url_for('final_check', account= 'user', random_pin= random_id))
        else:
            error = 'Invalid room-id or password. Please try again!'
    return render_template('login_page.html', error=error)

@app.route(f'/<account>/<random_pin>', methods=['POST', 'GET'])
def final_check(account, random_pin):
    global random_id
    if 'logged_in' in session and session.get('accessed_dashboard'):
        session.pop('accessed_dashboard', None)
        if account == "grand_admin" and random_pin == random_id:
            return render_template("grand_admin_page.html")
        if account == "admin" and random_pin == random_id:
            return render_template("admin_page.html")
        if account == "user" and random_pin == random_id:
            return render_template("user_page.html")
    else:
        return redirect(url_for('check_out'))
# Press the green button in the gutter to run the script.
#---------------------------Set Access--------------------------
@app.route('/set_pri_access', methods=['POST', 'GET'])
def pri_access():
    if request.method == 'POST':
        account = request.form['account']
        accessType = request.form['access_type']
        password = request.form['password']
        insertData(accessType, account, password)
        return render_template("primary_access.html", success=True)
    return render_template("primary_access.html", success=False)

@app.route('/set_sec_access', methods=['POST', 'GET'])
def grant_access():
    if request.method == 'POST':
        account = request.form['account']
        accessType= request.form['access_type']
        password = request.form['password']
        insertData(accessType, account, password)
    return render_template("secondary_access.html")
#-----------------------Delete Data---------------------
@app.route('/delete_sec_access', methods=['POST', 'GET'])
def delete_sec():

    return render_template("delete_secondary_access.html")
@app.route('/delete_pri_access', methods=['POST', 'GET'])
def delete_pri():
    return render_template("delete_primary_access.html")
#-----------------------Fetch Data-----------------------
@app.route('/fetchData', methods=['GET'])
def fetch_data():
    global pri_data, pri_category
    pri_category = request.args.get('category')
    pri_data = showData("")
    return jsonify(pri_data.get(pri_category, []))
@app.route('/submitData', methods=['POST'])
def submit_data():
    global pri_data, pri_category
    pri_data = request.get_json()
    pri_category = pri_data.get('category')
    selected_data = pri_data.get('dataList')
    del_data(pri_category, selected_data)
    return jsonify({'status': 'success', 'Jurisdiction': pri_category, 'Account': selected_data})

@app.route('/fetchData1', methods=['GET'])
def fetch_data1():
    global sec_data, sec_category
    sec_category = request.args.get('category')
    sec_data = showData("")
    return jsonify(sec_data.get(sec_category, []))
@app.route('/submitData1', methods=['POST'])
def submit_data1():
    global sec_data, sec_category
    sec_data = request.get_json()
    sec_category = sec_data.get('category')
    selected_data = sec_data.get('dataList')
    del_data(sec_category, selected_data)
    return jsonify({'status': 'success', 'Jurisdiction': sec_category, 'Account': selected_data})
#-------------------------------------TEST----------------------------------------------




#-------------------------Run Main---------------------
# if __name__ == '__main__':
#     app.run(host=f'{ipadd()}', debug=True, threaded=True)
# python web server
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
