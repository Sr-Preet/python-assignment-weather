from flask import Flask, render_template, request
from datetime import datetime
import requests

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route("/weatherapp", methods=["POST", "GET"])
def get_weatherdata():
    url="https://api.openweathermap.org/data/2.5/weather"

    params ={
        'q':request.form.get("city"),
        'appid':'a771e288754956cacb9456ec050c7e94',
        'units':'metric'
    }
    response=requests.get(url, params=params)
    data = response.json()
    city = data['name']
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    now = datetime.now()
    current_date = now.strftime("%d %b %Y")
    current_day = now.strftime("%A")


    return render_template('response.html', city=city, temperature=temperature, description=description, humidity=humidity, wind_speed=wind_speed, current_date=current_date, current_day=current_day)

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)