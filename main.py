from flask import Flask , render_template, request
from flask.templating import render_template
import mysql.connector
# from passlib.hash import sha256_crypt
drid = 0
nuid = 0
macid = 0
roomid = 0
techid = 0

mydb = mysql.connector.connect(
	host = 'localhost',
	username = 'root',
	passwd = '@Hm$d_2001',
	database = 'radiology')
mycursor = mydb.cursor()

app=Flask(__name__)

@app.route('/')
def index():
	return render_template('signin.html')     

@app.route('/doctor')
def doctor():
	return render_template('doctor.html')     

@app.route('/nurse')
def nurse():
	return render_template('nurse.html')     

@app.route('/home')
def home():
	return render_template('home.html')     

@app.route('/patient')
def patient():
	return render_template('patient.html')     
 
@app.route('/technician')
def technician():
	return render_template('technician.html')     

@app.route('/admin', methods=['GET', 'POST'])
def admin(): 
	if request.method == 'POST':
		fname = request.form['fname']
		minit = request.form['minit']
		lname = request.form['Lname']
		ssn = request.form['DSSN']
		address = request.form['address']
		pnumber = request.form.get('pnumber')
		qual = request.form.get('qualifications')
		gender = request.form['gender']
		bdate = request.form['bdate']
		relstatus = request.form['relstatus']
		sql = "INSERT INTO doctors (SSN, Name, ID, Address, PNumber, Qualifications, Gender, BDate, RelStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		global drid
		drid= drid+1
		val = ( ssn, (fname + " " + minit + " " + lname), drid, address, pnumber, qual, gender, bdate, relstatus)    
		mycursor.execute(sql, val)
		mydb.commit()
		return render_template('admin.html')
	else:
		return render_template('admin.html') 

@app.route('/admin/add-nurse', methods = ['GET', 'POST'])
def addnurse():
	if request.method == 'POST':
		fname = request.form['fname']
		minit = request.form['minit']
		lname = request.form['Lname']
		ssn = request.form['SSN']
		qual = request.form.get('qual')
		bdate = request.form['nBdate']
		address = request.form['address']
		pnumber = request.form.get('npnumber')
		email = request.form['email']
		global nuid
		nuid += 1
		sql = 'INSERT INTO nurses (Name, SSN, ID, BDate, Address, PNumber, Email) VALUES (%s, %s, %s, %s, %s, %s, %s)'
		val = ((fname + " " + minit + ' ' + lname), ssn, nuid, bdate, address, pnumber, email)
		mycursor.execute(sql, val)
		mydb.commit()
		return render_template('addnurse.html')
	else:
		return render_template('addnurse.html')
	

@app.route('/admin/add-machine', methods = ['GET', 'POST'])
def addmachine():
	if request.method == 'POST':
		global macid
		macid += 1
		mtype = request.form['type']
		mnumber = request.form['mnumber']
		cday = request.form['cday']
		purdate = request.form['purdate']
		sql = 'INSERT INTO machines(ID, Type, ModelNum, CheckDays, PurDate) VALUES(%s, %s, %s, %s, %s)'
		val = (macid, mtype, mnumber, cday, purdate)
		mycursor.execute(sql, val)
		mydb.commit()
		return render_template('addmachine.html')
	else:
		return render_template('addmachine.html')

@app.route('/admin/add-room', methods = ['GET', 'POST'])
def addroom():
	if request.method == 'POST':
		global roomid
		roomid += 1
		name = request.form['rname']
		sql = 'INSERT INTO rooms(Name, ID) VALUES (%s, %s)'
		val = (name, roomid)
		mycursor.execute(sql, val)
		mydb.commit()
		return render_template('addroom.html')
	else:
		return render_template('addroom.html') 

@app.route('/admin/add-technician', methods = ['GET', 'POST'])
def addtechnician():
	if request.method == 'POST':
		global techid
		techid += 1
		fname = request.form['fname']
		minit = request.form['minit']
		lname = request.form['Lname']
		ssn = request.form['DSSN']
		address = request.form['address']
		pnumber = request.form['tpnumber']
		email = request.form['email']
		bdate = request.form['bdate']
		sql = 'INSERT INTO technician(Name, SSN, ID, Address, PNumber, Email, BDate) VALUES (%s, %s, %s, %s, %s, %s, %s)'
		val = ((fname + ' ' + minit + ' ' + lname), ssn, techid, address, pnumber, email, bdate)
		mycursor.execute(sql, val)
		mydb.commit()
		return render_template('addtechnician.html')
	else:
		return render_template('addtechnician.html')   

@app.route('/doctor/patient-list')
def dview():
	return render_template('dview.html')    

@app.route('/doctor/report')
def dreport():
	return render_template('dreport.html') 


@app.route('/nurse/patient-list')
def nview():
	return render_template('nview.html') 
	
@app.route('/nurse/report-scan')
def nreport():
	return render_template('nreport.html')
		
@app.route('/nurse/report-machine')
def nmachine():
	return render_template('nmachine.html') 

@app.route('/patient/patient-scan-history')
def phistory():
	return render_template('phistory.html') 
	
@app.route('/patient/view-reservation')
def preservation():
	return render_template('preservation.html') 

@app.route('/technician/maintenance')
def tmaintenance():
	return render_template('tmain.html')

@app.route('/technician/checks')
def tchecks():
	return render_template('tchecks.html')     

@app.route('/technician/issues')
def tissues():
	return render_template('tissues.html') 

if __name__=='__main__':
	app.run(debug=True)