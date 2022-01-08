from flask import Flask, render_template, request, redirect, flash, url_for
from flask.templating import render_template
import mysql.connector
from DB import connect
from datetime import datetime
from functools import wraps
# connect()

isLoggedIn=False
type=''
mydb = mysql.connector.connect(
	host = 'localhost',
	username = 'root',
	passwd = '0504632240',
	database = 'radiology')
mycursor = mydb.cursor(buffered =True)

app=Flask(__name__)
app.config['SECRET_KEY'] = '54aaacc75d53041c924e22910015ddda'

@app.route('/', methods = ['POST', 'GET'])
@app.route('/signin', methods = ['POST', 'GET'])
def signin():
	if request.method == 'POST':
		user = request.form['username']
		passwd = request.form['password']
		# cred = (user, passwd, signtype)
		mycursor.execute("SELECT * FROM users WHERE username='" + user + "' and password='" + passwd + "'")
		data=mycursor.fetchone()
		render_template('doctor.html')	
		if data is not None:
			global type
			_,_,password,type=data
			print(password)
			if password==passwd:
				global isLoggedIn
				isLoggedIn=True
				if type =='d':
					flash('You are now logged in')
					return redirect(url_for('doctor'))
				elif type=='t':
					flash('You are now logged in')
					return redirect(url_for('technician'))
				elif type=='p':
					flash('You are now logged in')
					return redirect(url_for('patient'))
				elif type=='a':
					flash('You are now logged in')
					return redirect(url_for('admin'))
		else:
			flash('Wrong username or Password')
			return render_template('signin.html')
	else: 			
		return render_template('signin.html')

def is_logged_ind(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and type =='d':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap

def is_logged_int(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and type =='t':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap

def is_logged_inp(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and type =='p':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap	

def is_logged_inn(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and type =='n':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap	

def is_logged_ina(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and type =='a':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap		

@app.route('/doctor')
@is_logged_ind
def doctor():
	return render_template('doctor.html')     

@app.route('/nurse')
@is_logged_inn
def nurse():
	return render_template('nurse.html')     

@app.route('/home')
def home():
	return render_template('home.html')     

@app.route('/patient', methods=['POST', 'GET'])
@is_logged_inp
def patient():
	if request.method == 'POST':
		fname = request.form['fname']
		minit = request.form['minit']
		lname = request.form['lname']
		ssn = request.form['ssn']
		address = request.form['address']
		pnumber = request.form['pnumber']
		email = request.form['email']
		scantype = request.form['scantype']
		scandate = request.form['scandate']
		sql = 'INSERT INTO patients(FName, MInit, LName, SSN, ADDRESS, PNUMBER, EMAIL) VALUES (%s, %s, %s, %s, %s, %s, %s)'
		val = (fname, minit, lname, ssn, address, pnumber, email)
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('patient'))
	else:
		return render_template('patient.html')
 
@app.route('/technician')
@is_logged_int
def technician():
	return render_template('technician.html')     

@app.route('/admin', methods=['GET', 'POST'])
@is_logged_ina
def admin(): 
	if request.method == 'POST':
		fname = request.form['fname']
		minit = request.form['minit']
		lname = request.form['Lname']
		ssn = request.form['DSSN']
		address = request.form['address']
		email = request.form['email']
		pnumber = request.form['pnumber']
		gender = request.form['gender']
		bdate = request.form['Bdate']
		username = request.form['username']
		password = request.form['password']
		
		sql = 'INSERT INTO users(Username, Password, Type) VALUES (%s, %s, %s)'
		val = (username, password, 'd')
		mycursor.execute(sql,val)
		mydb.commit()
		
		sql = "SELECT Username, Password, Type FROM Users WHERE Username = %s"
		val = (username,)
		mycursor.execute(sql, val)
		user = mycursor.fetchone()
		sql1 = 'SELECT ID FROM Users WHERE Username=%s'
		val1 = (username,)
		mycursor.execute(sql1, val1)
		id = mycursor.fetchone()
		print('ID IS EQUAL TO %s', id)
		sql = "INSERT INTO doctors (SSN, FName, MInit, LName, ADDRESS, PNUMBER,  GENDER, BDATE, ID, EMAIL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		val = (ssn, fname, minit, lname, address, pnumber, gender, bdate, id[0], email)    
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('admin'))
	else:
		return render_template('admin.html') 

@app.route('/admin/add-nurse', methods = ['GET', 'POST'])
def addnurse():
	if request.method == 'POST':
		fname = request.form['fname']
		minit = request.form['minit']
		lname = request.form['Lname']
		ssn = request.form['SSN']
		bdate = request.form['nBdate']
		address = request.form['address']
		pnumber = request.form['npnumber']
		gender = request.form['gender']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		sql = 'INSERT INTO users(Username, Password, Type) VALUES (%s, %s, %s)'
		val = (username, password, 'n')
		mycursor.execute(sql,val)
		mydb.commit()
		sql1 = 'SELECT ID FROM Users WHERE Username=%s'
		val1 = (username,)
		mycursor.execute(sql1, val1)
		id = mycursor.fetchone()
		print('ID IS EQUAL TO', id)
		sql = 'INSERT INTO nurses (FName, MInit, LName, SSN, BDATE, ADDRESS, PNUMBER, EMAIL, GENDER, ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		val = (fname, minit, lname, ssn, bdate, address, pnumber, email, gender, id[0])
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('addnurse'))
	else:
		return render_template('addnurse.html')
	

@app.route('/admin/add-machine', methods = ['GET', 'POST'])
def addmachine():
	if request.method == 'POST':
		mtype = request.form['type']
		mnumber = request.form['mnumber']
		cday = request.form['cday']
		purdate = request.form['purdate']
		sql = 'INSERT INTO machines(TYPE, MODELNO, CHECKDAYS, PURDATE) VALUES(%s, %s, %s, %s)'
		val = (mtype, mnumber, cday, purdate)
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('addmachine'))
	else:
		return render_template('addmachine.html')

@app.route('/admin/add-room', methods = ['GET', 'POST'])
def addroom():
	if request.method == 'POST':
		name = request.form['rname']
		type = request.form['type']
		sql= "SELECT ID FROM machines WHERE TYPE=%s AND IN_USE='0'"
		val = (type,)
		mycursor.execute(sql, val)
		id = mycursor.fetchone()
		sql = 'INSERT INTO rooms(NAME, MACHINE_ID) VALUES (%s, %s)'
		val = (name, id[0])
		mycursor.execute(sql, val)
		mydb.commit()
		sql = "UPDATE machines SET IN_USE = '1' WHERE ID = %s"
		val = (id[0],)
		mycursor.execute(sql,val)
		mydb.commit()
		return redirect(url_for('addroom'))
	else:
		return render_template('addroom.html') 

@app.route('/admin/add-technician', methods = ['GET', 'POST'])
def addtechnician():
	if request.method == 'POST':
		fname = request.form['fname']
		minit = request.form['minit']
		lname = request.form['Lname']
		ssn = request.form['DSSN']
		address = request.form['address']
		pnumber = request.form['pnumber']
		gender = request.form['gender']
		bdate = request.form['bdate']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		sql = 'INSERT INTO users(Username, Password, Type) VALUES (%s, %s, %s)'
		val = (username, password, 't')
		mycursor.execute(sql,val)
		mydb.commit()
		sql1 = 'SELECT ID FROM Users WHERE Username=%s'
		val1 = (username,)
		mycursor.execute(sql1, val1)
		id = mycursor.fetchone()
		sql = "INSERT INTO technicians (SSN, FName, MInit, LName, ADDRESS, PNUMBER,  GENDER, BDATE, ID, EMAIL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		val = (ssn, fname, minit, lname, address, pnumber, gender, bdate, id[0], email)    
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('addtechnician'))
	else:
		return render_template('addtechnician.html')   

@app.route('/doctor/patient-list', methods = ['POST', 'GET'])
def dview():
	if request.method == 'POST':
		return redirect(url_for('doctor'))
	else:
		mycursor.execute('SELECT * FROM patients')
		rowheaders = [x[0] for x in mycursor.description]
		print(rowheaders)
		res = mycursor.fetchall()
		data = {
			'rowheaders': rowheaders,
			'res': res}
		return render_template('dview.html', data = data)    


@app.route('/nurse/patient-list')
def nview():
	return render_template('nview.html') 
	

		
@app.route('/nurse/report-machine')
def nmachine():
	return render_template('nmachine.html') 

@app.route('/patient/patient-scan-history')
def phistory():
	return render_template('phistory.html') 
	
@app.route('/patient/view-reservation')
def preservation():
	return render_template('preservation.html') 


@app.route('/technician/checks')
def tchecks():
	return render_template('tchecks.html')     

@app.route('/technician/issues')
def tissues():
	return render_template('tissues.html') 

if __name__=='__main__':
	app.run(debug=True)
