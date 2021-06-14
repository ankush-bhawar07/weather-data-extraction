import requests
import mysql.connector
from datetime import datetime

# data extraction
user_api = "4c4c334f055a2b046735e186fe6fbe2a"
location = input("Enter the city name ")
complet_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+user_api


api_link = requests.get(complet_api_link)
api_data = api_link.json()
print(api_data)



if api_data["cod"] == "404":
    print("Invalid City: {}, Please check your City name".format(location))
else:
    temp_city = ((api_data["main"]["temp"]) - 273.15)
    weather_desc = api_data["weather"][0]["description"]
    hmdt = api_data["main"]["humidity"]
    wind_spd = api_data["wind"]["speed"]
    date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")


    # inserting data into database
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='root')
    mycursor = mydb.cursor()


    mycursor.execute("DROP DATABASE weather")
    mycursor.execute("CREATE DATABASE weather;")
    mycursor.execute("use weather;")
    mycursor.execute("CREATE TABLE weatherdata( locationdb varchar(25) PRIMARY KEY,temp_citydb DECIMAL, weather_descdb VARCHAR(25),hmdtdb INT,wind_spddb DECIMAL,date_timedb VARCHAR(25));")
    mycursor.execute("INSERT INTO weatherdata VALUES (%s, %s, %s, %s, %s, %s)", (location, temp_city, weather_desc,hmdt,wind_spd,date_time))

    mydb.commit()
    mycursor.close()