# from install_libraries import *
import requests
from requests.exceptions import RequestException
from location_api_ava import *


class Weather:
    def __init__(self, camp_id, temperature, humidity, wind_speed, description, main_weather):
        self.camp_id = camp_id
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.description = description
        self.main_weather = main_weather 

        

    def fetch_weather(lat, lon, api_key):

        try:
   
            openweathermap_api_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
            weather_check = requests.get(openweathermap_api_weather_url)
   
    
            if  weather_check.status_code == 200:
                weather = weather_check.json()

                if weather:
                    temperature = weather["main"]["temp"]
                    humidity = weather["main"]["humidity"]
                    wind_speed = weather["wind"]["speed"]
                    description = weather["weather"][0]["description"]
                    main_weather = weather["weather"][0]["main"]
                #print(weather)
                    return temperature, humidity, wind_speed, description, main_weather
                else:
                    return None
    
            else:
                return f"HTTP error: {weather_check.status_code}"
        except RequestException as error:
            return f"An error occured during the weather API request: {error}"
    
    #def input_weather(camp_id):
        #input_camp_id = int(input("Enter camp id:"))
        #return Weather(camp_id, weather_result)



#api_key = "9d6ccb7de466e40be62e06d6f4a01d13"
#city_name = input("Enter city name:")
#state_code = input ("Enter state code:")
#country_code = input("Enter country code:")
#weather_result = Weather.fetch_weather(location_results[0],location_results[1],"9d6ccb7de466e40be62e06d6f4a01d13" )
#print(f"Weather: {weather_result}")
