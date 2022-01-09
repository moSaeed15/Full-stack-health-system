from flask import Flask, render_template, request, redirect, flash, url_for
from flask.templating import render_template
import mysql.connector
from datetime import datetime
from functools import wraps
import pandas as pd
from scanassgn import scanassign

isLoggedIn=False
typeL=''
totalHrs=0
currentuser=''
mydb = mysql.connector.connect(
	host = 'localhost',
	username = 'root',
	passwd = '@Hm$d_2001',
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
		if data is not None:
			global typeL
			_,_,password,typeL=data
			print(password)
			if password==passwd:
				global isLoggedIn
				global currentuser
				currentuser = user
				isLoggedIn=True
				if typeL =='d':
					flash('You are now logged in')
					return redirect(url_for('doctor'))
				elif typeL=='t':
					flash('You are now logged in')
					return redirect(url_for('technician'))
				elif typeL=='p':
					flash('You are now logged in')
					return redirect(url_for('patient'))
				elif typeL=='a':
					flash('You are now logged in')
					return redirect(url_for('admin'))
				elif typeL=='n':
					flash('You are now logged in')
					return redirect(url_for('nurse'))				
		else:
			flash('Wrong username or Password')
			return render_template('signin.html')
	else: 			
		return render_template('signin.html')

def is_logged_ind(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and typeL =='d':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap

def is_logged_int(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and typeL =='t':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap

def is_logged_inp(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and typeL =='p':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap	

def is_logged_inn(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and typeL =='n':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap	

def is_logged_ina(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and typeL =='a':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap		
    

@app.route('/home')
def home():
	global typeL
	if typeL =='a':
		return redirect(url_for('admin'))
	elif typeL=='p':
		return redirect(url_for('patient'))
	elif typeL=='d':
		return redirect(url_for('doctor'))
	elif typeL=='t':
		return redirect(url_for('technician'))
	elif typeL=='n':
		return redirect(url_for('nurse'))
	else:
		flash('Unauthorized, Please login')
		return redirect(url_for('signin'))


@app.route('/registerp', methods=['POST', 'GET'])
def registerp():
	if request.method == 'POST':
		fname = request.form['fname']
		minit = request.form['minit']
		lname = request.form['lname']
		ssn = request.form['ssn']
		address = request.form['address']
		pnumber = request.form['pnumber']
		email = request.form['email']
		gender = request.form['gender']
		bdate = request.form['bdate']
		username = request.form['username']
		password = request.form['password']
		
		sql = 'INSERT INTO users(Username, Password, Type) VALUES (%s, %s, %s)'
		val = (username, password, 'p')
		mycursor.execute(sql,val)
		mydb.commit()

		sql1 = 'SELECT ID FROM Users WHERE Username=%s'
		val1 = (username,)
		mycursor.execute(sql1, val1)
		id = mycursor.fetchone()

		sql = 'INSERT INTO patients(FName, MInit, LName, SSN, ADDRESS, PNUMBER, EMAIL, ID, GENDER, BDATE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		val = (fname, minit, lname, ssn, address, pnumber, email, id[0], gender, bdate)
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('signin'))
	else:
		return render_template('registerp.html')

@app.route('/patient', methods=['POST', 'GET'])
def patient():
	if request.method == 'POST':
		scantype = request.form['Mtype']
		scandate = request.form['scandate']
		print(type(scandate))

		sql1 = 'SELECT ID FROM Users WHERE Username=%s'
		global currentuser
		print(currentuser)
		val1 = (currentuser,)
		mycursor.execute(sql1, val1)
		id = mycursor.fetchone()
		
		#Scan assignment system
		scanassign(scandate, scantype, id)
		
		return redirect(url_for('patient'))
	else:
		return render_template('patient.html')
     

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
		hours = request.form['hours']
		username = request.form['username']
		password = request.form['password']
		
		sql = 'INSERT INTO users(Username, Password, Type) VALUES (%s, %s, %s)'
		val = (username, password, 'd')
		mycursor.execute(sql,val)
		mydb.commit()
		
		sql1 = 'SELECT ID FROM Users WHERE Username=%s'
		val1 = (username,)
		mycursor.execute(sql1, val1)
		id = mycursor.fetchone()
		print('ID IS EQUAL TO %s', id)
		sql = "INSERT INTO doctors (SSN, FName, MInit, LName, ADDRESS, PNUMBER,  GENDER, BDATE, ID, EMAIL, HOURS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		val = (ssn, fname, minit, lname, address, pnumber, gender, bdate, id[0], email, hours)    
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
		hours = request.form['hours']
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
		sql = 'INSERT INTO nurses (FName, MInit, LName, SSN, BDATE, ADDRESS, PNUMBER, EMAIL, GENDER, ID, HOURS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		val = (fname, minit, lname, ssn, bdate, address, pnumber, email, gender, id[0], hours)
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('addnurse'))
	else:
		return render_template('addnurse.html')
	

@app.route('/admin/add-machine', methods = ['GET', 'POST'])
def addmachine():
	if request.method == 'POST':
		mtype = request.form['Mtype']
		mnumber = request.form['mnumber']
		cday = request.form['cday']
		purdate = request.form['purdate']
		sql = 'INSERT INTO machines(TYPE, MODELNO, CHECKDAYS, PURDATE, IN_USE) VALUES(%s, %s, %s, %s, %s)'
		val = (mtype, mnumber, cday, purdate, 0)
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('addmachine'))
	else:
		return render_template('addmachine.html')

@app.route('/admin/add-room', methods = ['GET', 'POST'])
def addroom():
	if request.method == 'POST':
		name = request.form['rname']
		type = request.form['Mtype']
		sql= "SELECT ID FROM machines WHERE TYPE=%s AND IN_USE='0'"
		val = (type,)
		mycursor.execute(sql, val)
		id = mycursor.fetchone()
		sql = 'INSERT INTO rooms(NAME, MACHINE_ID, HOURS) VALUES (%s, %s, %s)'
		val = (name, id[0], 24)
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



@app.route('/doctor', methods=['POST', 'GET'])
@is_logged_ind
def doctor():
	if 	request.method == 'POST':
		case = request.form['data']
		diag = request.form['diag']
		mycursor.execute(f'DELETE FROM current_scans WHERE ID={case}')
		mydb.commit()
		mycursor.execute(f'UPDATE Scan_History SET DIAGNOSIS={diag}')
		mydb.commit()
		redirect(url_for('doctor'))
	else:
		global currentuser
		mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
		resid = mycursor.fetchone()
		mycursor.execute(f'''
			SELECT Patients.FName, Patients.LName, current_scans.DATE, current_scans.TYPE
			FROM current_scans
			JOIN Patients On current_scans.PAT_ID=Patients.ID
			JOIN Doctors On current_scans.DR_ID=Doctors.ID
			WHERE current_scans.DR_ID='{resid[0]}'
			ORDER BY DATE ASC
		''')
		res = mycursor.fetchall()
		mycursor.execute(f'''
			SELECT current_scans.ID
			FROM current_scans
			JOIN Patients On current_scans.PAT_ID=Patients.ID
			JOIN Doctors On current_scans.DR_ID=Doctors.ID
			WHERE current_scans.DR_ID='{resid[0]}'
			ORDER BY DATE ASC
		''')
		val = mycursor.fetchall()
		data = val + res
		print(type(data))
		x = len(val)
		print(x)
		return render_template('doctor.html', data=data, x=int(x))
	
@app.route('/doctor/patient-list', methods = ['POST', 'GET'])
def dview():
	if request.method == 'POST':
		return redirect(url_for('doctor'))
	else:
		global currentuser
		mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
		resid = mycursor.fetchone()
		mycursor.execute(f'''
		SELECT Patients.FName, Patients.LName, current_scans.TYPE, current_scans.DATE
		FROM Patients 
		JOIN current_scans On Patients.ID=current_scans.PAT_ID
		JOIN Doctors On current_scans.DR_ID=Doctors.ID
		JOIN Users On Doctors.ID=Users.ID
		WHERE current_scans.DR_ID = '{resid[0]}'
		ORDER BY DATE ASC''') 
		rowheaders = ['First Name', 'Last Name', 'Scan Type', 'Scan Date']
		res = mycursor.fetchall()
		print(rowheaders, res, currentuser)
		data = {
			'rowheaders': rowheaders,
			'res': res}
		return render_template('dview.html', data = data)    



@app.route('/nurse')
@is_logged_inn
def nurse():
	return render_template('nurse.html')     

@app.route('/nurse/patient-list')
def nview():
	if request.method == 'POST':
		return redirect(url_for('nurse'))
	else:
		global currentuser
		mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
		resid = mycursor.fetchone()
		mycursor.execute(f'''
		SELECT Patients.FName, Patients.LName, current_scans.TYPE, current_scans.DATE
		FROM Patients 
		JOIN current_scans On Patients.ID=current_scans.PAT_ID
		JOIN Nurses On current_scans.NUR_ID=Nurses.ID
		JOIN Users On Nurses.ID=Users.ID
		WHERE current_scans.NUR_ID = '{resid[0]}'
		ORDER BY DATE ASC''') 
		rowheaders = ['First Name', 'Last Name', 'Scan Type', 'Scan Date']
		res = mycursor.fetchall()
		print(rowheaders, res, currentuser)
		data = {
			'rowheaders': rowheaders,
			'res': res}
		return render_template('nview.html', data = data)    
		
@app.route('/nurse/report-machine')
def nmachine():
	return render_template('nmachine.html') 



@app.route('/patient/patient-scan-history')
def phistory():
	if request.method == 'POST':
		return redirect(url_for('patient'))
	else:
		global currentuser
		mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
		resid = mycursor.fetchone()
		mycursor.execute(f'''
		SELECT Doctors.FName, Doctors.LName, Nurses.FName, Nurses.LName, current_scans.TYPE, current_scans.DATE
		FROM Scan_History
		JOIN Patients On Scan_History.PAT_ID=Patients.ID
		JOIN Nurses On Scan_History.NUR_ID=Nurses.ID
		JOIN Doctors On Scan_History.DR_ID=Doctors.ID
		JOIN Users On Patients.ID=Users.ID
		WHERE Scan_History.PAT_ID = '{resid[0]}'
		ORDER BY DATE ASC''')
		rowheaders = ['Dr First Name', 'Dr Last Name', 'Nurse First Name', 'Nurse Last Name','Scan Type', 'Scan Date']
		res = mycursor.fetchall()
		print(rowheaders, res, currentuser)
		data = {
			'rowheaders': rowheaders,
			'res': res}
		return render_template('phistory.html', data = data)    
	
@app.route('/patient/view-reservation')
def preservation():
	if request.method == 'POST':
		return redirect(url_for('patient'))
	else:
		global currentuser
		mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
		resid = mycursor.fetchone()
		mycursor.execute(f'''
		SELECT Doctors.FName, Doctors.LName, Nurses.FName, Nurses.LName, current_scans.TYPE, current_scans.DATE
		FROM Patients 
		JOIN current_scans On Patients.ID=current_scans.PAT_ID
		JOIN Nurses On current_scans.NUR_ID=Nurses.ID
		JOIN Doctors On current_scans.DR_ID=Doctors.ID
		JOIN Users On Patients.ID=Users.ID
		WHERE  AND current_scans.PAT_ID = '{resid[0]}'
		ORDER BY DATE ASC''') 
		rowheaders = ['Dr First Name', 'Dr Last Name', 'Nurse First Name', 'Nurse Last Name','Scan Type', 'Scan Date']
		res = mycursor.fetchall()
		print(rowheaders, res, currentuser)
		data = {
			'rowheaders': rowheaders,
			'res': res}
		return render_template('preservation.html', data = data) 


 
@app.route('/technician')
@is_logged_int
def technician():
	return render_template('technician.html')

@app.route('/technician/checks')
def tchecks():
	return render_template('tchecks.html')     

@app.route('/technician/issues')
def tissues():
	return render_template('tissues.html') 



if __name__=='__main__':
@	app.run(debug=True)