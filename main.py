import requests
import mysql.connector
from datetime import datetime
from flask import Flask, render_template
from flask import request
import json

# creating flask app
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
    user_api = "4c4c334f055a2b046735e186fe6fbe2a"
    location = request.form['location']
    ip_address = request.remote_addr
    complet_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+user_api
    api_link = requests.get(complet_api_link)
    api_data = api_link.json()

    if api_data["cod"] == "404" or location == "":
        return render_template('index.html', err="Please check your City name", )

    else:
        temp_city = ((api_data["main"]["temp"]) - 273.15)
        temp_city = "{:.2f}".format(temp_city)
        weather_desc = api_data["weather"][0]["description"]
        hmdt = api_data["main"]["humidity"]
        wind_spd = api_data["wind"]["speed"]
        date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

        # inserting data into database
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='root')
        mycursor = mydb.cursor()
        mycursor.execute("use weather;")
        mycursor.execute("INSERT INTO weatherdata VALUES (%s, %s, %s, %s, %s, %s, %s)", (ip_address, location, temp_city, weather_desc,hmdt,wind_spd,date_time))
        mydb.commit()
        mycursor.close()
        
        return render_template('index.html', date_time=date_time, temp_city=temp_city, weather_desc=weather_desc,hmdt=hmdt,wind_spd=wind_spd)

# geting rcords from database
@app.route("/dashboard")
def dashboard():
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='root')
        mycursor = mydb.cursor()
        mycursor.execute("use weather;")
        mycursor.execute("SELECT * FROM weatherdata;")
        dataFromDb = mycursor.fetchall()

        destructureData = []
        for i in range(len(dataFromDb)):
            result_t = []
            for x in dataFromDb[i]:
                result_t.append(str(x))
            destructureData.append(result_t)

        mydb.commit()
        mycursor.close()
        return render_template('dashboard.html', myresult=destructureData)

    # debugging
if __name__ == "__main__":
    app.run(debug=True)