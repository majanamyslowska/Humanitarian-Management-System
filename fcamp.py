from connectdb import *
from location_api_ava import city_coordinate_converter
from countries import get_country_code
from weather_api_ava import Weather
from weather_suggestions import check_temp


class Camp:

    def __init__(self, hp_id: str, country: str, city_name: str, capacity: int, total_refugees: int, total_volunteers: int, status: str, resources_state: str, totalGF: int, totalDF: int, totalNN: int, totalVgn: int, totalVgt: int, totalOmn: int, totalSP: int, temperature, humidity, wind_speed, description, main_weather):
        self.hp_id = hp_id  # change - confirm hp id in input field
        self.country = country
        self.city_name = city_name
        self.capacity = capacity
        self.total_refugees = total_refugees
        self.total_volunteers = total_volunteers
        self.status = status
        self.resources_state = resources_state
        self.totalGF = totalGF
        self.totalDF = totalDF  
        self.totalNN = totalNN  
        self.totalVgn = totalVgn
        self.totalVgt = totalVgt
        self.totalOmn = totalOmn
        self.totalSP = totalSP
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.description = description
        self.main_weather = main_weather
        
        

    
    def create_camp(self):
        with setup_conn() as conn:
            cursor = conn.cursor()
            data = (self.hp_id, self.country, self.city_name, self.capacity, self.total_refugees, self.total_volunteers, self.status, self.resources_state, self.totalGF, self.totalDF, self.totalNN, self.totalVgn, self.totalVgt, self.totalOmn, self.totalSP, self.temperature, self.humidity, self.wind_speed, self.description, self.main_weather )
            insert_query(cursor, 'camps', data)
            conn.commit()


def delete_camp_by_id():  # called to delete a specific camp AND when a hp is deleted
    camp_id = get_id_for_removal()
    with setup_conn() as conn:
        cursor = conn.cursor()
        remove_query2(cursor, 'camps', 'campID', camp_id)


def delete_camp_by_hp(hp_id):
    with setup_conn() as conn:
        cursor = conn.cursor()
        remove_query2(cursor, 'camps', 'planID', hp_id)


def transfer_or_delete_people():
    camp_id = get_id_for_removal()
    print("\nWould you like to transfer the refugees and volunteers to a differnt camp before deleting it? (Yes/No) ")
    print("1. Yes")
    print("2. No")
    answer = int(input("\nChoose an option: "))

    if answer == 1:
        new_camp = input("\nWhich camp ID would you like to transfer the refugees to? ")
        transfer_camp_r_v(camp_id, new_camp) # transfer before deleting
        with setup_conn() as conn:
            cursor = conn.cursor()
            remove_query2(cursor, 'camps', 'campID', camp_id)
        print("\nCamp has been successfully deleted and refugees and volunteers transfered.")
    
    elif answer == 2:
        with setup_conn() as conn:
            cursor = conn.cursor()
            remove_query2(cursor, 'camps', 'campID', camp_id)
        print("\nCamp has been successfully deleted.")


def create_camp_input_hp(hp_id):
    input_capacity = int(input("Enter camp capacity: "))
    input_status = input("Enter camp status: ")
    input_country = input("Enter country: ")
    input_city_name = input("Enter camp city: ")
    location_results = city_coordinate_converter(input_city_name, get_country_code(input_country), "5cd7288030c7b77ae8ef6fdca18ac418" )
    weather_result = Weather.fetch_weather(location_results[0],location_results[1],"9d6ccb7de466e40be62e06d6f4a01d13" )
    temperature, humidity, wind_speed, description, main_weather = weather_result
    print(f"The weather in {input_city_name} is: {weather_result}")
    print(f"The coordinates of this city are: {location_results}")
    return Camp(hp_id, input_country, input_city_name, input_capacity, 0, 0, input_status, '', 0, 0, 0, 0, 0, 0, 0, temperature, humidity, wind_speed, description, main_weather)

def create_camp_input():
    input_hp_id = int(input("Enter plan ID: "))
    input_capacity = int(input("Enter camp capacity: "))
    input_status = input("Enter camp status: ")
    input_country = input("Enter country: ")
    input_city_name = input("Enter campy city: ")
    location_results = city_coordinate_converter(input_city_name, get_country_code(input_country), "5cd7288030c7b77ae8ef6fdca18ac418" )
    weather_result = Weather.fetch_weather(location_results[0],location_results[1],"9d6ccb7de466e40be62e06d6f4a01d13" )
    temperature, humidity, wind_speed, description, main_weather = weather_result
    return Camp(input_hp_id, input_country, input_city_name, input_capacity, 0, 0, input_status, '', 0, 0, 0, 0, 0, 0, 0,temperature, humidity, wind_speed, description, main_weather)

#def weather_input(camp_id):
    #return 
    
### update
def update_total_count():
    # update refugee and volunteer count in the camps table
    camp_id = get_id_for_update() ### SESSION
    with setup_conn() as conn:
        cursor = conn.cursor()
        count_v_data = get_count(cursor, 'users', 'campID', camp_id)
        # count_r_data = get_count(cursor, 'refugees', 'campID', camp_id)
        update_by_column(cursor, 'camps', 'totalVolunteers', 'campID', camp_id, count_v_data)
        # update_by_column(cursor, 'camps', 'totalRefugees', camp_id, count_r_data)


def update_camp_status(new_status):
    camp_id = get_id_for_status()
    # print(camp_id, new_status)
    with setup_conn() as conn:
        cursor = conn.cursor()
        update_camp_status_f(cursor, camp_id, new_status)
        # update_by_column(cursor,'camps','status', camp_id, 'campID', new_status)


def get_id_for_removal():
    camp_id = int(input("\nEnter the ID of the camp to be removed: "))
    return camp_id


def get_id_for_status():
    camp_id = int(input("\nEnter the ID of the camp whose status you want to be updated: "))
    return camp_id


def get_id_for_update():
    camp_id = int(input("\nEnter the ID of the camp to be updated: "))
    return camp_id


# things to do:
# once the refugees and volunteers and resources are assigned, update the table
# eg. count query for number of refugees that were added to the camp, same with vs
# for resources the default should be 'enough' but everytime the resources table is updated,
# the camp table should be updated as well

# if needed to pull the last input id use plan_id = cursor.lastrowid

'''
error handling:
- cap the number of camps one can create within a hp - not sure
- make sure the number of refugees doesnt exceed the capacity
- confirming the hp - should exist (during creating a hp)
- when adding a new camp ensure it is added to an existing hp
- input types
- what happens here when hp closes
- finish resources state
- prompt the next thing that happens after a function about the camp is called
'''
