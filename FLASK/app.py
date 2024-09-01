from flask import Flask,jsonify,request
import requests,psycopg2,os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
app = Flask(__name__)

# Database configration and connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}:{os.getenv("port")}/{os.getenv("dbname")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing SQLAlchemy
db = SQLAlchemy(app)
class Weather(db.Model):
    """creating a model for the weather table"""

    __tablename__ = 'weather'
    id = db.Column(db.Integer,primary_key=True)
    city = db.Column(db.String,nullable=False)
    country = db.Column(db.String,nullable=False)
    temperature = db.Column(db.Float,nullable=False)
    description = db.Column(db.String,nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# route for get weather data for a particular city
@app.route('/get-weather/',methods=['POST'])
def get_weather():
    
    # getting data needed to make the request
    data = request.get_json() 
    # data = {
    #     'city': input('Enter a name of a city: ')
    # }
    city = data['city']
    api_key = os.getenv('API_KEY')
 
    if not city: # making sure a city name is provided
        return jsonify({'error':'please provide a name of a city'}),400
    
    if not isinstance(city,str): # data type validation 
        return jsonify({'error':'city name must be a sring '}),400 

    try:
        weather_url= f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

        # passing collected data into variables
        responds = requests.get(weather_url)
        weather_data = responds.json()
        country = weather_data['sys']['country']
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        date = weather_data['dt']

        #inserting collected data into the weather table
        new_city_date = Weather(city=city, country=country, temperature=temperature, description=description, date= db.func.to_timestamp(date))
        db.session.add(new_city_date)
        db.session.commit()
        
        return jsonify({'message':f'weather data for {city} has been collected.'}),200 # message to show the request was successful
   
    except (Exception,psycopg2.Error) as e:
        return jsonify({'error':str(e)}),500 

@app.route('/get-data/')
def get_data():
    """getting the stored data from the database and displaying it"""
    
    try:

        db_data = Weather.query.all() # fetching all data from db and displaying them

        if not db_data: # checking if the database is empty
            return({'message':'no data in the dababase'})
        
        all_data = [] # list for storing a dict for each city and it data    
        for data in db_data:
            weather_data = {
                'city' : data.city,
                'country' : data.country,
                'temperature': data.temperature,
                'description': data.description,
                'date':data.date
            }
            all_data.append(weather_data) 
        return jsonify({'Weather data': all_data}),200
    
    except (Exception,psycopg2.Error) as e:
        return jsonify({'Error': str(e)}),500

if __name__ == '__main__':
    app.run(debug=True)

