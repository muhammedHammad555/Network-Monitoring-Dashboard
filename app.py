from flask import Flask, render_template, redirect, url_for, Response, request, session
from scanner import scan_network
import json
import csv
import io

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

# الصفحة الرئيسية
@app.route('/')
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    devices = scan_network()

    online_count = sum(1 for device in devices if device["status"] == "Online")
    offline_count = sum(1 for device in devices if device["status"] == "Offline")

    return render_template(
        "index.html",
        devices=devices,
        online_count=online_count,
        offline_count=offline_count
    )

# صفحة تسجيل الدخول
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form["password"]
        if password == "0000":
            session['logged_in'] = True
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid password")
    return render_template("login.html")

# حذف جهاز من الشبكة
@app.route('/delete/<ip>')
def delete_device(ip):
    try:
        with open("devices.json", "r") as file:
            devices = json.load(file)

        if ip in devices:
            del devices[ip]

        with open("devices.json", "w") as file:
            json.dump(devices, file, indent=4)

    except:
        pass

    return redirect(url_for('home'))

# تصدير البيانات إلى ملف CSV
@app.route('/export')
def export_csv():
    devices = scan_network()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Device Name", "IP Address", "MAC Address", "Status", "Last Seen"])

    for d in devices:
        writer.writerow([
            d["name"],
            d["ip"],
            d["mac"],
            d["status"],
            d["last_seen"]
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition":"attachment;filename=network_report.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)