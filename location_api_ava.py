# from install_libraries import *
import requests
from countries import get_country_code
from requests.exceptions import RequestException




def city_coordinate_converter(city_name, country_code, api_key, state_code="N/A"):
    limit = 2

    try:
        openweathermap_api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={api_key}"
        coordinates_check = requests.get(openweathermap_api_url)
    
    
        if coordinates_check.status_code == 200:
            coordinates = coordinates_check.json()

            if coordinates:

                return coordinates[0]["lat"], coordinates[0]["lon"]
            else:
                return None
        
        else:
            return None, None
    except RequestException as error:
        return None, None
    
        #else:
            #return f"Coordinates for {city_name},{state_code},{country_code} not found"



#api_key = "5cd7288030c7b77ae8ef6fdca18ac418"
#city_name = input("Enter city name:")
#state_code = input ("Enter state code:")
#country_code = input("Enter country code:")
#location_results = city_coordinate_converter("Barcelona", get_country_code("Spain"), "5cd7288030c7b77ae8ef6fdca18ac418" )
#print(f"Coordinates: {location_results}")
