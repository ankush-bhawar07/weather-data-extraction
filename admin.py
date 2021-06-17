import mysql.connector
   
mydb = mysql.connector.connect(host='localhost', user='root', passwd='root')
mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE weather")
mycursor.execute("CREATE DATABASE weather;")
mycursor.execute("use weather;")
mycursor.execute("CREATE TABLE weatherdata( ip_address VARCHAR(25), location varchar(25), temp_city DECIMAL(4,2), weather_desc VARCHAR(25),hmdt INT,wind_spd DECIMAL(4,2), date_time VARCHAR(25));")

mydb.commit()
mycursor.close()