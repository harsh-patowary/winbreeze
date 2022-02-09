from crypt import methods
from curses import flash
import requests
import json
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'harsh004'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    img_url = "static/def-img.png"
    if request.method == 'POST':
        city = request.form['city']
        if not city:
            flash("City is required!")
        else:
            data = get_weather(city)
            if data.get('cod') != 200:
                message = data.get('message', '')
                flash(f"Error getting city data for {city} Error message = {message}")
            print(data)
            weather= (data.get('weather'))
            print(weather)
            F = round(data['main']['temp'])
            temp = round(F-273.15)
            humidity = data['main']['humidity']
            wind_speed =  data['wind']['speed']
            weather_img_id = data['weather'][0]['icon']
            img_url = f"http://openweathermap.org/img/wn/{weather_img_id}@2x.png"
            desc = data['weather'][0]['main']

            return render_template('weather.html', temp=temp, humidity=humidity, wind_speed=wind_speed, city=city, img_url=img_url, desc=desc)

    return render_template('weather.html', img_url=img_url)
    

def get_weather(c):

    API_KEY = 'dbccf151f4a62027a14fc792f54c5514'  # initialize your key here
    city = c  # city name passed as argument

    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
    response = requests.get(url)

    print(type(response.json()))
    print(response.json())
    return response.json()


