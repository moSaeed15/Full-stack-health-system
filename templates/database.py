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