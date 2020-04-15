from flask import Flask
from flask import render_template
from flask import request


import requests
import pandas as pd
import re


appid = "9253b6f1e7514bef9be055032b45b851"

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/myweather', methods=['GET', 'POST'])
def get_weather():
    if request.method == 'POST':
        input_city = request.form['myname']
        
        try:
            city_db = pd.read_json(path_or_buf='city_list.json')
            city_id = city_db[city_db['name'] == input_city].head(1)['id']
        except:
            return render_template('error.html', err_text="Incorrect city_list parsing")
        
        if city_id.empty == False:  
            try:
                
                url = f'api.openweathermap.org/data/2.5/weather?id={city_id}&appid={appid}'
                request_result = requests.get(url).json()
        
                current_temp = request_result['main']['temp']
                current_pressure = request_result['main']['pressure']
                current_humidity = request_result['main']['humidity']
                current_wind = request_result['wind']['speed']
            
 
        
                if re.fullmatch(r'\d+\.*\d*', str(current_temp)) == None:
                    return render_template('error.html', err_text="Incorrect Data Format")
                
                if re.fullmatch(r'\d+\.*\d*', str(current_pressure)) == None:
                    return render_template('error.html', err_text="Incorrect Data Format")
                
                if re.fullmatch(r'\d+\.*\d*', str(current_humidity)) == None:
                    return render_template('error.html', err_text="Incorrect Data Format")
                
                if re.fullmatch(r'\d+\.*\d*', str(current_wind)) == None:
                    return render_template('error.html', err_text="Incorrect Data Format")
                
                current_temp = current_temp - 273.15
                
                return render_template('weather.html', myname = input_city, current_temp = current_temp, current_pressure = current_pressure,  current_humidity = current_humidity, current_wind = current_wind  )
        
            except:
                return render_template('error.html', err_text="Incorrect DB parsing")
        else:
              return render_template('error.html', err_text="City is Unknown. Try another city")
        
    else:
        return render_template('error.html', err_text="Incorrect call")
    

if __name__ == '__main__':
    app.run()
    
    
   
    
    
            
    
    
    
    

