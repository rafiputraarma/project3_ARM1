import mysql.connector
import random, datetime, time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rafiarma08",
  database="monitoring"
)
mycursor = mydb.cursor()

def Menu():
    print("-----------TURBIN CRONTROL SIMULATOR------------")
    print("1. Data Temperatur")
    print("2. Data Pressure ")
    print("3. Data Temperatur & Pressure ")
    print("4. Emergency Stop")
    print("5. Exit Program")
   
    choice = int(input("Enter here: "))

    if(choice==1):
        for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(2)
            temperature1 = random.randint(55,65)
            temperature2 = temperature1 + 15
            status = "WORK"
            
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO monitoring_tbl (datetime, status, temp_inlet, temp_outlet) VALUES (%s, %s, %s, %s)", (date_time, status, temperature1, temperature2))
            mydb.commit()
            print(mycursor.rowcount, "Temperatur Turbin Terdeteksi...")

    if(choice==2):
        for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(1.5)
            pressure1 = random.randint(85,100)
            pressure2 = pressure1 + 15
            status = "2"
            
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO monitoring_tbl (datetime, status, pressure_inlet, pressure_outlet) VALUES (%s, %s, %s, %s)", (date_time, status, pressure1, pressure2))
            mydb.commit()
            print(mycursor.rowcount, "Pressure Turbin Terdeteksi...")

    if(choice==3):
        for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(1.5)
            temperature1 = random.randint(50,70)
            temperature2 = temperature1 + 15
            pressure1 = random.randint(85,100)
            pressure2 = pressure1 + 15
            status = "GOOD WORKING"
            
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO monitoring_tbl (datetime, status, temp_inlet, temp_outlet, pressure_inlet, pressure_outlet) VALUES (%s, %s, %s, %s, %s, %s)", (date_time, status, temperature1, temperature2, pressure1, pressure2))
            mydb.commit()
            print(mycursor.rowcount, "Temperatur & Pressure Turbin Terdeteksi...")  

    if(choice==5):
        exit()
        print(mycursor.rowcount, "Program Stop")

Menu()


