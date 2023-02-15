from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
mydb = mysql.connector.connect(
        host = '127.0.0.1',
        user = 'root',
        password = '',
        database = 'stdregister'
    )
cursor = mydb.cursor()
# https://www.xnxx.com/search/pussy?top

@app.route('/insert', methods=['POST', 'GET'])
def insert():
    if request.method == 'POST':
        name = request.form["fullName"]
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']

        cursor.execute("SELECT * FROM stdinfo WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            return render_template('regis.html', user=True)
        else:
            cursor.execute("Insert into stdinfo (name, email,mobile,password)value(%s,%s,%s,%s)", (name,email,mobile,password))
            mydb.commit()

            cursor.close()
            
            return redirect('/homee')
    return render_template('regis.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

@app.route('/homee')
def homee():
    user = cursor.fetchone()
    if 'email' in session:
        return render_template('landing.html', user=user)
    else:
        return redirect('/home')

@app.route('/logging', methods=['GET', 'POST'])
def logging():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM stdinfo WHERE email=%s AND password=%s", (email,password))
        user = cursor.fetchone()
        if user:
            session['email'] = email
            return redirect('/homee')
        else:
            return redirect('/logging')
    return render_template('login.html', user=True)

 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/regis')
def registration():
    return render_template('regis.html')

@app.route('/')
@app.route('/home')
def home():
    # if 'email' in session:
    return render_template('index.html')
    # else:
        # return redirect('/login')
if __name__ == '__main__':
    app.secret_key = "19874bb75ae54672aa36b88dd5d09675"
    app.run(debug=True)