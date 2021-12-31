from flask import Flask , render_template
from flask.templating import render_template
# from passlib.hash import sha256_crypt
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')     

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')     

@app.route('/nurse')
def nurse():
    return render_template('nurse.html')     

@app.route('/signin')
def signin():
    return render_template('signin.html')     

@app.route('/patient')
def patient():
    return render_template('patient.html')     


@app.route('/machine')
def machine():
    return render_template('machines.html')     


@app.route('/technician')
def technician():
    return render_template('technician.html')     

@app.route('/room')
def rooms():
    return render_template('rooms.html')     

if __name__=='__main__':
    app.run(debug=True)


