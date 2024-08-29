from flask import Flask,jsonify,request
import requests,psycopg2,os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def db_connect():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("dbname"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port")
        )
        print('message : connected to database')
        return connection
    except (Exception,psycopg2.Error) as e:
        print(f'error: {e} occured')

@app.route('/get-weather/',methods=['POST'])
def get_weather():

    data = request.get_json()
    city = data['city']
    api_key = os.getenv('API_KEY')

    weather_url= f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    try:
        responds = requests.get(weather_url)
        weather_data = responds.json()
        country = weather_data['sys']['country']
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        date = weather_data['dt']

        conn = db_connect()
        cur = conn.cursor()
        cur.execute('INSERT INTO weather (city,country,temperature,description,date) VALUES (%s,%s,%s,%s,%s)',(city,country,temperature,description,date))
        conn.commit()
        
        return jsonify({'message':f'weather data for {city} has been collected.'}),200
    except (Exception,psycopg2.Error) as e:
        return jsonify({'error':str(e)}),500
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)

