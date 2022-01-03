from flask import Flask , render_template, request
from flask.templating import render_template
import mysql.connector
# from passlib.hash import sha256_crypt

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
		val = ( ssn, (fname + minit + lname), 3, address, pnumber, qual, gender, bdate, relstatus)    
		mycursor.execute(sql, val)
		mydb.commit()
		return render_template('admin.html')
	else:
		return render_template('admin.html') 

@app.route('/admin/add-nurse')
def addnurse():
	return render_template('addnurse.html')    
	

@app.route('/admin/add-machine')
def addmachine():
	return render_template('addmachine.html')    

@app.route('/admin/add-room')
def addroom():
	return render_template('addroom.html')    

@app.route('/admin/add-technician')
def addtechnician():
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