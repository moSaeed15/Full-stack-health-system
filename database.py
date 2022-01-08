import mysql.connector;

config= {
    'user':'root',
    'password': '0504632240',
    'host':'localhost',
    'database':'radiology'
}   

db=mysql.connector.connect(**config)
cursor=db.cursor()

cursor.execute()



# if request.method == 'POST':
# 		user = request.form['username']
# 		passwd = request.form['password']
# 		cur=mysql.connection.cursor()	
# 		signtype = request.form['type']
# 		cred = (user, passwd, signtype)
# 		mycursor.execute('SELECT Username, Password, Type FROM users')
# 		check = mycursor.fetchall()
# 		if cred in check:
# 			flash(f'Successfully signed in as { user }')
# 			if signtype == 't':
# 				return redirect(url_for('technician'))
# 			elif signtype == 'a':
# 				return redirect(url_for('admin'))
# 			elif signtype == 'd':
# 				return redirect(url_for('doctor'))
# 			elif signtype == 'n':
# 				return redirect(url_for('nurse'))
# 		else:
# 			return redirect(url_for('signin'))
# 	return render_template('signin.html')