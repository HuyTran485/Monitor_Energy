# app.py hoặc routes.py
import socket
from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for, session, make_response

app = Flask(__name__)

# Chỉ init Firebase một lần
if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\FPT\Desktop\Monitor_Energy\json_key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://monitor-energy-767f1-default-rtdb.asia-southeast1.firebasedatabase.app'
    })
@app.route('/')
def admin_page():
    return render_template('admin_page.html')  # Đảm bảo file admin.html nằm trong /templates

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

if __name__ == '__main__':
    app.run(debug=True)