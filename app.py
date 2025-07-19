import socket
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for, session, make_response
import json
import os
import threading
from project_function import *
from datetime import datetime, timedelta
#--------------------------Declare variables-------------------
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
#---------------------------Log out function-----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('check_out'))
#---------------------------Login page--------------------
@app.route('/', methods=['POST', 'GET'])
def check_out():
    grand_admin_list = get_key_value(showData("/GrandAdmin"))
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
            session['account'] = account
            session['authority'] = "Admin"
            return redirect(url_for('final_check', authority="Admin",account=session['account'],
                                    random_pin=session['random_pin']))
        elif check_pass(account, password, user_list):
            # random_id = generate_random_string(40)
            session['random_pin'] = generate_random_string(40)
            session['logged_in'] = True
            session['accessed_dashboard'] = True
            room_id = find_room_by_account(user_data,account)
            session['account'] = account
            session['authority'] = room_id
            return redirect(url_for('final_check',authority=session['authority'],
                                    account=session['account'], random_pin=session['random_pin']))
        elif check_pass(account, password, grand_admin_list):
            # random_id = generate_random_string(40)
            session['random_pin'] = generate_random_string(40)
            session['logged_in'] = True
            session['accessed_dashboard'] = True
            room_id = find_room_by_account(user_data, account)
            session['account'] = account
            session['authority'] = "GrandAdmin"
            return redirect(url_for('final_check', authority="GrandAdmin",account=session['account'],
                                    random_pin=session['random_pin']))
        else:
            error = 'Invalid room-id or password. Please try again!'
    return render_template('login_page.html', error=error)
@app.route('/<authority>/<account>/<random_pin>', methods=['POST', 'GET'])
def final_check(authority,account, random_pin):
    if session.get('logged_in') and session.get('random_pin') == random_pin:
        if authority == 'Admin' and session.get('account') == account:
            return render_template("admin_page.html")
        elif authority == 'GrandAdmin' and session.get('account') == account:
            return render_template("grand_admin_page.html")
        elif authority in ["Room_1", "Room_2", "Room_3"] and session.get('account') == account:
            return render_template("user_page.html", authority=session['authority'],
                                    account=session['account'], random_pin=session['random_pin'] )
    return redirect(url_for('check_out'))
@app.route('/firebase_data')
def firebase_data():
    ref = db.reference('/')
    snapshot = ref.get()
    if snapshot is None:
        return jsonify({"error": "No data found"}), 404
    return jsonify({
        "User": snapshot.get("User", {})
    })
@app.route('/firebase_data_1')
def firebase_data_1():
    ref = db.reference('/')
    snapshot = ref.get()
    if snapshot is None:
        return jsonify({"error": "No data found"}), 404
    return jsonify({
        "Admin": snapshot.get("Admin", {}),
        "User": snapshot.get("User", {})
    })
#---------------------------Set Access--------------------------
@app.route('/<authority>/<account>/<random_pin>/set_pri_access', methods=['POST', 'GET'])
def set_pri_access(authority,account, random_pin):
    if request.method == 'POST':
        account_new = request.form['account']
        accessType = request.form['room_id']
        password = request.form['password']
        insertUser(accessType, account_new, password)
        return render_template("primary_access.html", success=True)
    return render_template("primary_access.html", success=False)

@app.route('/<authority>/<account>/<random_pin>/set_secondary_access', methods=['POST', 'GET'])
def set_secondary_access(authority,account, random_pin):
    if request.method == 'POST':
        if request.form['user_type'] == "User":
            account_new = request.form['account']
            accessType = request.form['room_id']
            password = request.form['password']
            insertUser(accessType, account_new, password)
        else:
            account_new = request.form['account']
            accessType = request.form['user_type']
            password = request.form['password']
            insertAccount(accessType, account_new, password)
        return render_template("secondary_access.html", success=True)
    return render_template("secondary_access.html", success=False)
#------------------------Delete account----------------------------------------
@app.route('/<authority>/<account>/<random_pin>/delete_pri_access', methods=['POST', 'GET'])
def delete_pri_access(authority,account, random_pin):
    return render_template("delete_primary_access.html")
@app.route('/<authority>/<account>/<random_pin>/delete_secondary_access', methods=['POST', 'GET'])
def delete_secondary_access(authority,account, random_pin):
    return render_template("delete_secondary_access.html")
@app.route('/<authority>/<account>/<random_pin>/reset_pass_2nd', methods=['POST', 'GET'])
def reset_pass_2nd(authority,account, random_pin):
    return render_template("reset_pass_2nd.html")
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
    account = data.get('account')
    category = data.get('category')
    if category == "User":
        room = data.get('room')
        del_user_data(category, room, account)
        return jsonify({'status': 'success', 'category': category, 'room': room, 'account': account})
    else:
        del_admin_data(category, account)
        return jsonify({'status': 'success', 'category': category, 'account': account})
@app.route('/resetPassword', methods=['POST'])
def reset_password():
    data = request.json
    category = data.get('category')
    account = data.get('account')

    if category == 'Admin':
        path = f'Admin/{account}'
    elif category == 'User':
        room = data.get('room')
        path = f'User/{room}/{account}'
    else:
        return jsonify({'error': 'Invalid category'}), 400

    # Firebase: cập nhật lại mật khẩu
    ref = db.reference(path)
    if ref.get() is None:
        return jsonify({'error': 'Account not found'}), 404

    ref.update({'Password': '000000'})
    return jsonify({'status': 'success'})

#-------------------------------------TEST----------------------------------------------
@app.route("/get_data", methods=["POST"])
def get_data():
    data = request.get_json()
    room_id = data.get("room_id")
    print(room_id)
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
    streamData = get_stream_data(room_id)
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
                        "total_cost": round(total_energy * 3500, 2),
                        "voltage": voltage,  # Không có dữ liệu điện áp
                        "current": current,  # Không có dữ liệu dòng điện
                        "power": power,
                        "pf": power_factor
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
@app.route('/fetch_data_range', methods=['POST', 'GET'])
def fetch_data_range():
    data = request.get_json()
    authority = data.get("authority")
    print(f"Rdata: {data}")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not authority or not start_date or not end_date:
        return jsonify({"error": "Thiếu dữ liệu đầu vào."}), 400

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        if start > end:
            return jsonify({"error": "Ngày bắt đầu phải trước hoặc bằng ngày kết thúc."}), 400
    except ValueError:
        return jsonify({"error": "Định dạng ngày không hợp lệ."}), 400

    total_energy = 0.0
    current = start
    while current <= end:
        y, m, d = current.year, current.month, current.day
        path = f"Data/{authority}/{y}/{m}/{d}"
        ref = db.reference(path)
        day_data = ref.get()

        if day_data:
            for hour, values in day_data.items():
                try:
                    e = float(values.get("Energy", 0))
                    total_energy += e
                except:
                    continue
        current += timedelta(days=1)

    total_cost = round(total_energy * 3500, 2)

    return jsonify({
        "total_energy": round(total_energy, 2),
        "total_cost": total_cost
    })
@app.route("/get_monthly_energy", methods=["POST"])
def get_monthly_energy():
    data = request.get_json()
    authority = data.get("authority")
    year = data.get("year")

    if not authority or not year:
        return jsonify({"error": "Thiếu authority hoặc năm."}), 400

    monthly_energy = []
    for month in range(1, 13):
        path = f"Data/{authority}/{year}/{month}/TotalEnergy"
        ref = db.reference(path)
        value = ref.get()
        try:
            monthly_energy.append(float(value))
        except:
            monthly_energy.append(0.0)

    return jsonify({ "monthly_energy": monthly_energy })

@app.route('/<authority>/<account>/<random_pin>/get_data_range', methods=['POST', 'GET'])
def get_data_range(authority, account, random_pin):
    session['authority'] = authority
    session['account'] = account
    session['random_pin'] = random_pin
    return render_template("range.html", authority=session['authority'],
                                    account=session['account'], random_pin=session['random_pin'])
@app.route('/<authority>/<account>/<random_pin>/chart_monthly', methods=['POST', 'GET'])
def chart_monthly(authority, account, random_pin):
    session['authority'] = authority
    session['account'] = account
    session['random_pin'] = random_pin
    return render_template("chart_monthly.html", authority=session['authority'],
                                    account=session['account'], random_pin=session['random_pin'])
#---------------------------Get daily energy
@app.route('/<authority>/<account>/<random_pin>/chart_daily_energy', methods=['GET'])
def chart_daily_energy(authority, account, random_pin):
    session['authority'] = authority
    session['account'] = account
    session['random_pin'] = random_pin
    return render_template("chart_daily_month.html", authority=authority,
                           account=account, random_pin=random_pin)

@app.route('/get_daily_energy_by_month', methods=['POST'])
def get_daily_energy_by_month():
    data = request.get_json()
    room_id = data.get("room_id")
    month = int(data.get("month"))
    year = int(data.get("year"))

    if not room_id or not month or not year:
        return jsonify({"error": "Thiếu room_id, month hoặc year"}), 400

    from calendar import monthrange
    days_in_month = monthrange(year, month)[1]
    daily_energy = []
    labels = []

    for day in range(1, days_in_month + 1):
        path = f"Data/{room_id}/{year}/{month}/{day}"
        ref = db.reference(path)
        data_day = ref.get()
        total = 0.0

        if data_day:
            for hour_data in data_day.values():
                try:
                    total += float(hour_data.get("Energy", 0))
                except:
                    continue

        labels.append(str(day))
        daily_energy.append(round(total, 2))

    daily_cost = [round(e * 3500, 2) for e in daily_energy]

    return jsonify({
        "labels": labels,
        "energy": daily_energy,
        "cost": daily_cost
    })

#-------------------------Run Main---------------------
if __name__ == '__main__':
    app.run(host=f'{ipadd()}', debug=True, threaded=True)
# python web server
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))  # Railway sẽ cấp PORT
#     app.run(host="0.0.0.0", port=port)
