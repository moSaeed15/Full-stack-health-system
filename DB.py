import mysql.connector


def connect():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="@Hm$d_2001",
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Radiology")
    mydb.commit()

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="@Hm$d_2001",
      database='Radiology'
    )
    mycursor = mydb.cursor()

    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS Users (
        ID INT NOT NULL UNIQUE AUTO_INCREMENT,
        Username VARCHAR(255) NOT NULL UNIQUE,
        Password VARCHAR(60) NOT NULL UNIQUE,
        Type VARCHAR(1) NOT NULL,
        PRIMARY KEY(ID)
      );
    ''')
    mydb.commit()
    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS Patients (
        ID INT NOT NULL UNIQUE,
        FName VARCHAR(255) NOT NULL,
        MInit VARCHAR(255),
        LName VARCHAR(255) NOT NULL,
        SSN INT NOT NULL UNIQUE,
        GENDER VARCHAR(45) NOT NULL,
        PNUMBER INT NOT NULL,
        EMAIL VARCHAR(255) NOT NULL,
        BDATE DATE NOT NULL,
        ADDRESS VARCHAR(255) NOT NULL,
        PRIMARY KEY(SSN),
        CONSTRAINT FK_ID
          FOREIGN KEY(ID)
          REFERENCES Users (ID)
      );
    ''')
    mydb.commit()
    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS current_scans (
        ID INT NOT NULL UNIQUE AUTO_INCREMENT,
        PAT_ID INT NOT NULL UNIQUE,
        TYPE VARCHAR(45) NOT NULL,
        DATE DATE NOT NULL,
        PRIMARY KEY(ID),
        CONSTRAINT FK_ID6
          FOREIGN KEY(PAT_ID)
          REFERENCES Patients (ID)
      )
    ''')
    mydb.commit()
    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS Doctors (
        ID INT NOT NULL UNIQUE,
        FName VARCHAR(255) NOT NULL,
        MInit VARCHAR(255),
        LName VARCHAR(255) NOT NULL,
        SSN INT NOT NULL UNIQUE,
        GENDER VARCHAR(45) NOT NULL,
        PNUMBER INT NOT NULL UNIQUE,
        EMAIL VARCHAR(255) NOT NULL UNIQUE,
        BDATE DATE NOT NULL,
        ADDRESS VARCHAR(255) NOT NULL,
        PRIMARY KEY(SSN),
        CONSTRAINT FK_ID1
          FOREIGN KEY(ID)
          REFERENCES Users (ID)
      );
    ''')
    mydb.commit()
    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS Nurses (
        ID INT NOT NULL UNIQUE,
        FName VARCHAR(255) NOT NULL,
        MInit VARCHAR(255),
        LName VARCHAR(255) NOT NULL,
        SSN INT NOT NULL UNIQUE,
        GENDER VARCHAR(45) NOT NULL,
        PNUMBER INT NOT NULL UNIQUE,
        EMAIL VARCHAR(255) NOT NULL UNIQUE,
        BDATE DATE NOT NULL,
        ADDRESS VARCHAR(255) NOT NULL,
        PRIMARY KEY(SSN),
        CONSTRAINT FK_ID2
          FOREIGN KEY(ID)
          REFERENCES Users (ID)
      );
    ''')
    mydb.commit()
    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS Technicians (
        ID INT NOT NULL UNIQUE,
        FName VARCHAR(255) NOT NULL,
        MInit VARCHAR(255),
        LName VARCHAR(255) NOT NULL,
        SSN INT NOT NULL UNIQUE,
        GENDER VARCHAR(45) NOT NULL,
        SPEC VARCHAR(45) NOT NULL,
        PNUMBER INT NOT NULL UNIQUE,
        EMAIL VARCHAR(255) NOT NULL UNIQUE,
        BDATE DATE NOT NULL,
        ADDRESS VARCHAR(255) NOT NULL,
        PRIMARY KEY(SSN),
        CONSTRAINT FK_ID3
          FOREIGN KEY(ID)
          REFERENCES Users (ID)
      );
    ''')
    mydb.commit()
    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS Admins (
        ID INT NOT NULL UNIQUE,
        FName VARCHAR(255) NOT NULL,
        MInit VARCHAR(255),
        LName VARCHAR(255) NOT NULL,
        SSN INT NOT NULL UNIQUE,
        GENDER VARCHAR(45) NOT NULL,
        PNUMBER INT NOT NULL UNIQUE,
        EMAIL VARCHAR(255) NOT NULL UNIQUE,
        BDATE DATE NOT NULL,
        ADDRESS VARCHAR(255) NOT NULL,
        PRIMARY KEY(SSN),
        CONSTRAINT FK_ID4
          FOREIGN KEY(ID)
          REFERENCES Users (ID)
      );
    ''')
    mydb.commit()
    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS Scan_History (
        PAT_ID INT NOT NULL UNIQUE,
        TYPE VARCHAR(45) NOT NULL,
        DATE DATE NOT NULL,
        PRIMARY KEY(ID),
        CONSTRAINT FK_ID5
          FOREIGN KEY(PAT_ID)
          REFERENCES Patients (ID)
      );
    ''')
    mydb.commit()
    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS Machines (
        ID INT NOT NULL UNIQUE AUTO_INCREMENT,
        MODELNO INT NOT NULL,
        TYPE VARCHAR(45) NOT NULL,
        PURDATE DATE NOT NULL,
        CHECKDAYS INT NOT NULL,
        PRIMARY KEY(ID)
      );
    ''')
    mydb.commit()
    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS Changes (
        ID INT NOT NULL UNIQUE AUTO_INCREMENT,
        ADMIN_ID INT NOT NULL UNIQUE,
        DETAILS VARCHAR(255) NOT NULL,
        DATETIME DATETIME(0) NOT NULL,
        PRIMARY KEY(ID),
        CONSTRAINT FK_ADMIN
          FOREIGN KEY (ADMIN_ID)
          REFERENCES Admins (ID)
      );
    ''')
    mydb.commit()
    mycursor.execute('''
      CREATE TABLE IF NOT EXISTS Rooms (
        ID INT NOT NULL UNIQUE AUTO_INCREMENT,
        NAME VARCHAR(255),
        MACHINE_ID INT NOT NULL UNIQUE,
        DR_ID INT NOT NULL UNIQUE,
        NURSE_ID INT NOT NULL UNIQUE,
        PAT_ID INT NOT NULL UNIQUE,
        AVALAIBLE BOOL NOT NULL,
        PRIMARY KEY(ID),
        CONSTRAINT FK_MACHINE
          FOREIGN KEY (MACHINE_ID)
          REFERENCES Machines (ID),
        CONSTRAINT FK_DOCTOR
          FOREIGN KEY (DR_ID)
          REFERENCES Doctors (ID),
        CONSTRAINT FK_NURSE
          FOREIGN KEY (NURSE_ID)
          REFERENCES Nurses (ID),
        CONSTRAINT FK_PATIENT
          FOREIGN KEY (PAT_ID)
          REFERENCES Patients (ID)
      );
    ''')
    mydb.commit()

