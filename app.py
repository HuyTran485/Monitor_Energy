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
    admin_list = get_key_value(showData("/Admin"))
    user_data = showData("/User")
    user_list = get_key_value_1(user_data)
    error = None
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        if check_pass(account, password, admin_list):
            # random_id = generate_random_string(40)
            session['random_pin'] = generate_random_string(40)
            session['logged_in'] = True
            session['accessed_dashboard'] = True
            session['account'] = 'admin'
            return redirect(url_for('final_check', account='admin', random_pin=session['random_pin']))
        elif check_pass(account, password, user_list):
            # random_id = generate_random_string(40)
            session['random_pin'] = generate_random_string(40)
            session['logged_in'] = True
            session['accessed_dashboard'] = True
            room_id = find_room_by_account(user_data,account)
            session['account'] = room_id
            return redirect(url_for('final_check', account=room_id, random_pin=session['random_pin']))
        else:
            error = 'Invalid room-id or password. Please try again!'
    return render_template('login_page.html', error=error)
@app.route('/<account>/<random_pin>', methods=['POST', 'GET'])
def final_check(account, random_pin):
    if session.get('logged_in') and session.get('random_pin') == random_pin:
        if account == 'admin' and session.get('account') == 'admin':
            return render_template("admin_page.html")
        elif account in ["Room_1", "Room_2", "Room_3"] and session.get('account') == account:
            return render_template("user_page.html", room_id=account)
    return redirect(url_for('check_out'))
@app.route('/firebase_data')
def firebase_data():
    ref = db.reference('/')
    snapshot = ref.get()
    if snapshot is None:
        return jsonify({"error": "No data found"}), 404
    return jsonify({
        "Admin": snapshot.get("Admin", {}),
        "User": snapshot.get("User", {})
    })

#---------------------------Set Access--------------------------
@app.route('/<account>/<random_pin>/set_pri_access', methods=['POST', 'GET'])
def set_pri_access(account, random_pin):
    if request.method == 'POST':
        account_new = request.form['account']
        accessType = request.form['room_id']
        password = request.form['password']
        insertUser(accessType, account_new, password)
        return render_template("primary_access.html", success=True)
    return render_template("primary_access.html", success=False)

# @app.route('/set_sec_access', methods=['POST', 'GET'])
# def grant_access():
#     if request.method == 'POST':
#         account = request.form['account']
#         accessType= request.form['access_type']
#         password = request.form['password']
#         insertUser(accessType, account, password)
#     return render_template("secondary_access.html")
#-----------------------Delete Data---------------------
# @app.route('/delete_sec_access', methods=['POST', 'GET'])
# def delete_sec():
#     return render_template("delete_secondary_access.html")
@app.route('/<account>/<random_pin>/delete_pri_access', methods=['POST', 'GET'])
def delete_pri_access(account, random_pin):
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
    data = request.get_json()
    category = data.get('category')
    room = data.get('room')
    account = data.get('account')
    # Gọi hàm xóa account cụ thể
    del_data(category, room, account)
    return jsonify({'status': 'success', 'category': category, 'room': room, 'account': account})

# @app.route('/fetchData1', methods=['GET'])
# def fetch_data1():
#     global sec_data, sec_category
#     sec_category = request.args.get('category')
#     sec_data = showData("")
#     return jsonify(sec_data.get(sec_category, []))
# @app.route('/submitData1', methods=['POST'])
# def submit_data1():
#     global sec_data, sec_category
#     sec_data = request.get_json()
#     sec_category = sec_data.get('category')
#     selected_data = sec_data.get('dataList')
#     del_data(sec_category, selected_data)
#     return jsonify({'status': 'success', 'Jurisdiction': sec_category, 'Account': selected_data})
#-------------------------------------TEST----------------------------------------------
@app.route("/get_data", methods=["POST"])
def get_data():
    data = request.get_json()
    room_id = data.get("room_id")
    date = data.get("date")
    if not room_id or not date:
        return jsonify({"error": "Thiếu room_id hoặc ngày."})
    try:
        # Chuyển định dạng ngày từ chuỗi sang đối tượng datetime (nếu cần)
        selected_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
        print(room_id, selected_date)
    except ValueError:
        return jsonify({"error": "Định dạng ngày không hợp lệ."})
    energy_data = get_energy_data(room_id, selected_date)
    print(energy_data)
    # ======= 🔽 Giả lập dữ liệu bạn lấy từ Firebase hoặc cơ sở dữ liệu =======
    # Giả sử dữ liệu lưu dưới dạng: data_store[room_id][ngày][giờ] = { ... }
    hours = []
    energy = []
    total_energy = 0
    streamData = get_stream_data("Room_1")
    current = streamData['current']
    power_factor = streamData['pf']
    power = streamData['power']
    voltage = streamData['voltage']
    total_energy = update_monthly_energy(room_id, selected_date)
    total_cost = round(total_energy * 3500, 2)  # 3500 VND/kWh
    try:
        for hour in sorted(energy_data.keys(), key=lambda x: int(x)):
            hour_label = f"{int(hour):02d}:00"
            e = float(energy_data[hour].get("Energy", 0))
            hours.append(hour_label)
            energy.append(e)

    except:
        return jsonify({"error": "Không có dữ liệu trong ngày này",
                        "hours": [],
                        "energy": [],
                        "total_energy": round(total_energy, 2),
                        "total_cost": 0,
                        })

    return jsonify({
        "hours": hours,
        "energy": energy,
        "total_energy": round(total_energy, 2),
        "total_cost": total_cost,
        "voltage": voltage,  # Không có dữ liệu điện áp
        "current": current,  # Không có dữ liệu dòng điện
        "power": power,
        "pf": power_factor
    })



#-------------------------Run Main---------------------
if __name__ == '__main__':
    app.run(host=f'{ipadd()}', debug=True, threaded=True)
# python web server
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))  # Railway sẽ cấp PORT
#     app.run(host="0.0.0.0", port=port)
