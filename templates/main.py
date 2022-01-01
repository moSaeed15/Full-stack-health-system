from flask import Flask , render_template
from flask.templating import render_template
# from passlib.hash import sha256_crypt
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

@app.route('/admin')
def admin():
    return render_template('admin.html')    

@app.route('/admin/add-nurse')
def addnurse():
    return render_template('addnurse.html')    


@app.route('/admin/add-doctor')
def addDoctor():
    return render_template('addDoctor.html')    

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
if __name__=='__main__':
    app.run(debug=True)


