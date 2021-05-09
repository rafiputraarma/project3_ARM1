# app.py

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import json
import random, datetime, time

app = Flask(__name__)
app.config['SECRET_KEY'] = "^A%DJAJU^JJ123"
app.config['MYSQL_HOST'] = 'rafiputraarma08.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'rafiputraarma08'
app.config['MYSQL_PASSWORD'] = 'pakhilmi'
app.config['MYSQL_DB'] = 'rafiputraarma08$finish'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/userhome')
def userhome():
    return render_template("userhome.html")



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM management_user WHERE name=%s", (name,))
        user = curl.fetchone()
        curl.close()

        if user  :
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return redirect ("/userlogin")
    else:
        return render_template("login.html")


@app.route('/userlogin', methods=["GET", "POST"])
def userlogin():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM management_user WHERE name=%s", (name,))
        user = curl.fetchone()
        curl.close()

        if user  :
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                return render_template("userhome.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("userlogin.html")


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO management_user (name, password) VALUES (%s,%s)",
                    (name, hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        return redirect(url_for('userhome'))

# User
@app.route('/management_user')
def user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM management_user")
    rv = cur.fetchall()
    cur.close()
    return render_template('management_user.html', users=rv)

@app.route('/simpan-management_user', methods=["POST"])
def saveUser():
    nama = request.form['nama']
    password = request.form['password']
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO management_user (name, password, status) VALUES (%s, %s, %s)", (nama, password, status))
    mysql.connection.commit()
    return redirect(url_for('user'))


@app.route('/update-management_user', methods=["POST"])
def updateUser():
    id_data = request.form['id']
    nama = request.form['nama']
    password = request.form['password']
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE management_user SET name=%s, password=%s, status=%s WHERE Id=%s", (nama, password, status, id_data,))
    mysql.connection.commit()
    return redirect(url_for('user'))

@app.route('/hapus-management_user/<string:id_data>', methods=["GET"])
def hapusUser(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM management_user WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('user'))
# end User

@app.route('/management_user1')
def user1():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM management_user")
    rv = cur.fetchall()
    cur.close()
    return render_template('management_user1.html', user1s=rv)


# js Monitoring
@app.route('/monitoring_tbl1')
def tbl1():
    return render_template("monitoring_tbl1.html")

@app.route('/monitoring_tbl')
def tbl():
    return render_template("monitoring_tbl.html")

@app.route('/turbin', methods= ['POST', 'GET'])
def turbin():
    curturbin = mysql.connection.cursor()
    curturbin.execute("SELECT * FROM monitoring_tbl")
    rvturbin = curturbin.fetchall()
    return jsonify(rvturbin=rvturbin)

@app.route('/delete', methods=["GET"])
def delete():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM management_user")
    mysql.connection.commit()
    return ('', 204)

@app.route('/clearlog', methods=["GET"])
def clearlog():
    cur = mysql.connection.cursor()
    for i in range (10):
            cur.execute("DELETE FROM monitoring_tbl")
            mysql.connection.commit()
    return ('', 204)

@app.route('/clearlogapp', methods=['POST','GET'])
def clearlogapp():
    logic = request.form['logic']
    if logic == '1':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM monitoring_tbl")
        mysql.connection.commit()
    return ('', 204)

@app.route('/stop', methods= ['GET'])
def stop():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM monitoring_tbl")
    for i in range(1):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(1)
            temperature1 = random.randint(20,26)
            temperature2 = temperature1
            pressure1 = "NORMAL"
            pressure2 = "NORMAL"
            status = "TURBIN OFF"

            cur.execute("INSERT INTO monitoring_tbl (datetime, status, temp_inlet, temp_outlet, pressure_inlet, pressure_outlet) VALUES (%s, %s, %s, %s, %s, %s)", (date_time, status, temperature1, temperature2, pressure1, pressure2))
            mysql.connection.commit()
            mysql.connection.commit()
    return ('', 204)

@app.route('/stopapp', methods= ['GET'])
def stopapp():
    logic = request.form['logic']
    if logic == '1':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM monitoring_tbl")
        for i in range(1):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(1)
            temperature1 = random.randint(20,26)
            temperature2 = temperature1
            pressure1 = "NORMAL"
            pressure2 = "NORMAL"
            status = "TURBIN OFF"

            cur.execute("INSERT INTO monitoring_tbl (datetime, status, temp_inlet, temp_outlet, pressure_inlet, pressure_outlet) VALUES (%s, %s, %s, %s, %s, %s)", (date_time, status, temperature1, temperature2, pressure1, pressure2))
            mysql.connection.commit()
            mysql.connection.commit()
    return ('', 204)

@app.route('/start', methods= ['POST','GET'])
def start():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM monitoring_tbl")
    for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(2)
            temperature1 = random.randint(50,70)
            temperature2 = temperature1 + 15
            pressure1 = random.randint(85,100)
            pressure2 = pressure1 + 15
            status = "GOOD WORKING"

            cur.execute("INSERT INTO monitoring_tbl (datetime, status, temp_inlet, temp_outlet, pressure_inlet, pressure_outlet) VALUES (%s, %s, %s, %s, %s, %s)", (date_time, status, temperature1, temperature2, pressure1, pressure2))
            mysql.connection.commit()
    return ('', 204)

@app.route('/startonapp', methods= ['POST','GET'])
def startonapp():
    logic = request.form['logic']
    if logic == '1':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM monitoring_tbl")
        for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(2)
            temperature1 = random.randint(50,70)
            temperature2 = temperature1 + 15
            pressure1 = random.randint(85,100)
            pressure2 = pressure1 + 15
            status = "GOOD WORKING"

            cur.execute("INSERT INTO monitoring_tbl (datetime, status, temp_inlet, temp_outlet, pressure_inlet, pressure_outlet) VALUES (%s, %s, %s, %s, %s, %s)", (date_time, status, temperature1, temperature2, pressure1, pressure2))
            mysql.connection.commit()
    return ('', 204)

@app.route('/temperatur', methods= ['POST','GET'])
def temperatur():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM monitoring_tbl")
    for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(2)
            temperature1 = random.randint(50,70)
            temperature2 = temperature1 + 15
            status = "WORK"

            cur.execute("INSERT INTO monitoring_tbl (datetime, status, temp_inlet, temp_outlet) VALUES (%s, %s, %s, %s)", (date_time, status, temperature1, temperature2))
            mysql.connection.commit()
    return ('', 204)

@app.route('/temperaturonapp', methods= ['POST','GET'])
def temperaturonapp():
    logic = request.form['logic']
    if logic == '1':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM monitoring_tbl")
        for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(2)
            temperature1 = random.randint(50,70)
            temperature2 = temperature1 + 15
            status = "WORK"

            cur.execute("INSERT INTO monitoring_tbl (datetime, status, temp_inlet, temp_outlet) VALUES (%s, %s, %s, %s)", (date_time, status, temperature1, temperature2))
            mysql.connection.commit()
    return ('', 204)

@app.route('/pressure', methods= ['POST','GET'])
def pressure():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM monitoring_tbl")
    for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(2)
            pressure1 = random.randint(85,100)
            pressure2 = pressure1 + 15
            status = "GOOD"

            cur.execute("INSERT INTO monitoring_tbl (datetime, status, pressure_inlet, pressure_outlet) VALUES (%s, %s, %s, %s)", (date_time, status, pressure1, pressure2))
            mysql.connection.commit()
    return ('', 204)

@app.route('/pressureonapp', methods= ['POST','GET'])
def pressureonapp():
    logic = request.form['logic']
    if logic == '1':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM monitoring_tbl")
        for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(2)
            pressure1 = random.randint(85,100)
            pressure2 = pressure1 + 15
            status = "GOOD"

            cur.execute("INSERT INTO monitoring_tbl (datetime, status, pressure_inlet, pressure_outlet) VALUES (%s, %s, %s, %s)", (date_time, status, pressure1, pressure2))
            mysql.connection.commit()
    return ('', 204)

@app.route('/TempPress')
def TempPress():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM monitoring_tbl")
    #row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    cur.close()
    return render_template('TempPress.html', temppress=rv)

@app.route('/temperaturapp')
def temperaturapp():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM monitoring_tbl")
    #row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    cur.close()
    return render_template('temperaturapp.html', temperaturapp=rv)

@app.route('/pressureapp')
def pressureapp():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM monitoring_tbl")
    #row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    cur.close()
    return render_template('pressureapp.html', pressureapp=rv)

#if __name__ == '__main__':
#    app.secret_key = "^A%DJAJU^JJ123"
#    app.run( debug=True)