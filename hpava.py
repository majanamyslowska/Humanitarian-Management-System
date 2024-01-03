from connectdb import setup_conn, insert_query, remove_query2, view_specific_row, edit_attribute, insert_end_date
#from optionsmenu import *
from hp_error import InvalidStartDateError, InvalidEndDateError, InvalidTypeInput, InvalidLocationInput
from datetime import datetime
import sqlite3


class HumanitarianPlan:
    type_list = ["Flood", "Fire", "Volcano", "Tsunami", "War", "Hurricane", "Earthquake", "Nuclear Disaster",
                 "Political Persecution"]
    location_list = ['Europe', 'South America', 'North America', 'Asia', 'Oceania', 'Africa']

    def __init__(self, type_index, description, location_index, campNo, start_date):
        self.type = type_index
        self.description = description
        self.location = location_index
        self.campNo = campNo
        self.start_date = start_date

        try:

            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            #end_datetime = datetime.strptime(end_date, "%d-%m-%Y")

            #if not isinstance(input_plan_id, int) or input_plan_id<0:
                #raise ValueError("Must only contain numbers")
                #if hp_id <0 :'''
                #raise ValueError("HP Id must be a positive integer")
            #if isinstance(hp_name, str):
                #raise NameError("Name must not contain numbers")
            if start_datetime < datetime.now():
                raise InvalidStartDateError()
            #if end_datetime < datetime.now():
                #raise InvalidEndDateError()
            #if end_datetime < start_datetime:
                #raise InvalidEndDateError()
            #if isinstance(location, str):
                #raise NameError("Location must not contain numbers")
        except InvalidStartDateError as error:
            print(error)
        #except InvalidEndDateError:
            #print(f"Invalid End date: {end_date} ")


    @classmethod
    def create_humanitarian_plan_menu(cls):

        print("Create humanitarian plan:\n")

        for option_no, type_option in enumerate(cls.type_list):
            print(f"{option_no}:{type_option}")

        input_type = int(input("\nEnter the option number that corresponds to your humanitarian plan type: "))

        ##Ava : error handling

        try:
            if input_type not in range(0,len(cls.type_list)-1):
                raise InvalidTypeInput("You must select an option number between 0-8")
        except InvalidTypeInput as error:
            print(error)


        for option_no, location_option in enumerate(cls.location_list):
            print(f"{option_no}:{location_option}")

        input_location = int(input("\nEnter the option number that corresponds to your humanitarian plan location: "))

        #Ava: Error handling

        try:
            if input_location not in range(0,len(cls.location_list)-1):
                raise InvalidLocationInput("You must enter an option number between 0-5")
        except InvalidLocationInput as error:
            print(error)

        input_description = input("\nEnter humanitarian plan description: ")

        #Ava: error handling

        try:
            if isinstance(input_description, str):
                raise NameError("Name must not contain numbers")
        except NameError as error:
            print(error)

        input_startdate = input("\nEnter humanitarian plan start date DD/MM/YYYY: ")

        
        try:

            start_datetime = datetime.strptime(input_startdate, "%d-%m-%Y")
            
            if start_datetime < datetime.now():
                raise InvalidStartDateError()
         
        except InvalidStartDateError as error:
            print(error)

        return cls(input_type, input_description, input_location, input_startdate)


    def delete_humanitarian_plan_menu():
        print("\nWelcome to the delete humanitarian plan menu")
        input_plan_ID = int(input("Enter planID: "))
        #Ava: error handling

        try:
            if not isinstance(input_plan_ID, int) or input_plan_ID<0:
    
                raise ValueError("planID must be a positive integer")
            
        except ValueError as error:
            print(error)
            
        
        return input_plan_ID

    def create_humanitarian_plan(plan):
        with setup_conn() as conn:
            cursor = conn.cursor()
            data = (plan.type, plan.description, plan.location, plan.campNo, plan.start_date)
            try:
                insert_query(cursor, 'humanitarianplan', data)
                conn.commit()
                if cursor.rowcount>0:
                    print(f"{plan} with {data} successfully created")
                else:
                    print("Executed but no changes made, ensure you have entered an existing planID")
            except sqlite3.Error as error:
                print(error)

    @staticmethod
    def delete_humanitarian_plan(input_plan_ID):
        with setup_conn() as conn:
            cursor = conn.cursor()
            theid = input_plan_ID

            try:
                remove_query2(cursor, 'humanitarianplan','planID', theid)
                conn.commit()
                if cursor.rowcount>0:
                    print(f"HP: {input_plan_ID} successfully deleted")
                else:
                    print("Executed but no changes made, ensure you have entered an existing planID")
            except sqlite3.Error as error:
                print(error)

        print(f"\nHumanitarian plan {input_plan_ID} has been succesfully deleted.") 
  
  
    def edit_humanitarian_plan(input_plan_id):
        planID = input_plan_id
        view_specific_row(planID, 'humanitarianplan')
        


    def close_humanitarian_plan_menu():
        print("\nWelcome to the close humanitarian plan menu!")
        input_plan_id = int(input("Enter the plan ID: "))
        end_date = input("Enter the end date: ")

        return end_date, input_plan_id

    def close_humanitarian_plan(end_date, input_plan_id):
        insert_end_date(end_date, input_plan_id)

    # edit_humanitarian_plan(int(input("Enter the planID which you want to edit:")))

    def edit_humanitarian_plan_menu(input_plan_id):
        print("-----------Welcome to the edit humanitarian plan menu------------------")
        # input_plan_id = int(input("Enter the planID which you want to edit:"))
        # edit_humanitarian_plan(int(input("Enter the planID which you want to edit:")))

        from optionsmenu import menu_edit_humanitarian_plan 
        choice = menu_edit_humanitarian_plan()

        match choice:

            case 1:
                for option_no, type_option in enumerate(HumanitarianPlan.type_list):
                    print(f"{option_no}:{type_option}")

                input_type = int(input("Enter the option number that corresponds to your humanitarian plan type: "))
                edit_attribute("type", HumanitarianPlan.type_list[input_type], input_plan_id)
                

            case 2:
                input_description = input("Enter humanitarian plan description: ")
                edit_attribute("description", input_description, input_plan_id)
                

            case 3:
                for option_no, location_option in enumerate(HumanitarianPlan.location_list):
                    print(f"{option_no}:{location_option}")

                input_location = int(
                    input("Enter the option number that corresponds to your humanitarian plan location: "))
                edit_attribute("location", HumanitarianPlan.location_list[input_location], input_plan_id)

            case 4:
                input_startdate = input("Enter humanitarian plan start date YYYY-MM-DD: ")
                edit_attribute("start_date", input_startdate, input_plan_id)





