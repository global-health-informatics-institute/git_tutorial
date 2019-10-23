#!/usr/bin/env python 

import RPi.GPIO as GPIO
import signal
import MySQLdb
import MFRC522
from time import gmtime, strftime 
from datetime import date
continue_reading = True

#String variable for names
first_name = ""
last_name = ""

#create DB object
db = MySQLdb.connect("localhost", "root", "NEWPASSWORD", "rfiddb")
#Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    
#Hook the SGINT
signal.signal(signal.SIGINT,end_read)

#Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

#Welcom massage
print ("Welcome to the RFID log in system")

#To check for chips
while continue_reading:
    
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQUDL)
    
    if status == MIFAREReader.MI_OK:
        print ("Card Detected")
pass

#Get the UID of the card
(status,_uid) = MIFAREReader.MFRC522_Anticoll()
#If we have the UID, continue    
if status == MIFAREReader.MI_OK:
    
    _uid = str(uid[0])+ "," + str(uid[1])+ "," + str(uid[2])+ "," + str(uid[3])
    print(_uid)
                                                                            
        
    cur = db.cursor();
    cur.execute("SELECT * FROM users WHERE uid = %s", (_uid,))
#Read data        
    for row in cur.fetchall():
        firstname = str (row[1])
        lastname = str (row[2])
#Read time and date
        _currTime = strtime("%H:%M:%S",gmtime())
        _currDate = date.today().strtime("%Y-%m-%d")
        
        print ("Hello"+firstname+""+lastname + _currDate+""+_currTime)
#Insert every log in into database
        try:
            try:
                cur.execute("INSERT INTO log(uid,first_name,last_name, _currTime, _currDate)VALUES (%s,%s,%s,%s)", (_uid,firstname,lastname,_currDate,_currTime))
                db.commit()
            except (db.Error, db.Warning) as e:
                print (e)
            finally:
                print ("Sucessful")
                cur.close()
                

#Default key authentication
        
                key=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
            
 
 #Select the scanned tags
                MIFAREReader.MFRC522_SelectTag (_uid)

                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, _uid)
        
#Authenticate
            if status == MIFAREReader.MI_OK:
                
                MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCryto1()
            else:
                print ("Authentication error")
                db.close()
                
        except (db.Error, db.Warning) as e:
                pass
                
                