from connectdb import setup_conn

class SchedulingSystem:
    @staticmethod
    def add_availability(volunteer, camp, day_of_week, start_time, end_time):
        with setup_conn() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM availability WHERE volunteer = ? AND campID = ? AND day_of_week = ? AND start_time = ? AND end_time = ?"
            cursor.execute(query, (volunteer, camp, day_of_week, start_time, end_time))
            existing_data = cursor.fetchone()

        with setup_conn() as conn:
            if existing_data is None:
                cursor = conn.cursor()
                query = "INSERT INTO availability (volunteer, campID, day_of_week, start_time, end_time) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(query, (volunteer, camp, day_of_week, start_time, end_time))
                print("\nNew working slot has been added.")

            else:
                print("Data already exists.")

    @staticmethod
    def delete_availability(volunteer, camp, day_of_week, start_time, end_time):
        with setup_conn() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM availability WHERE volunteer = ? AND campID = ? AND day_of_week = ? AND start_time = ? AND end_time = ?"
            cursor.execute(query, (volunteer, camp, day_of_week, start_time, end_time))
            existing_data = cursor.fetchone()

        with setup_conn() as conn:
            if existing_data is not None:
                cursor = conn.cursor()
                query = "DELETE FROM availability WHERE volunteer = ? AND campID = ? AND day_of_week = ? AND start_time = ? AND end_time = ?"
                cursor.execute(query, (volunteer, camp, day_of_week, start_time, end_time))
                print("\nWorking slot has been deleted.")

            else:
                print("Data not found. Nothing to delete.")


    @staticmethod
    def get_availability(session):
        with setup_conn() as conn:
            cursor = conn.cursor()
            query = "SELECT volunteer, day_of_week, start_time, end_time FROM availability WHERE volunteer = ?"
            cursor.execute(query, (session["username"],))   
            result = cursor.fetchall()

            if result is not None:
                print(result)

            else:
                ("\nNo data avaliable.")
                

    @staticmethod            
    def get_schedule_as_dict():
        schedule_dict = {}
        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT volunteer, campID, day_of_week, start_time, end_time FROM availability")

        for row in cursor.fetchall():
            volunteer_name, day_of_week, start_time, end_time = row
            if day_of_week not in schedule_dict:
                schedule_dict[day_of_week] = []

            schedule_dict[day_of_week].append({
                'volunteer': volunteer_name,
                'start_time': start_time,
                'end_time': end_time
            })

        if schedule_dict is not None:
            print(schedule_dict)

        else:
            ("\nNo data avaliable.")

scheduling_system = SchedulingSystem()

def edit_availability(session):
    print("What would you like to edit?")
    print("1. Add a working time slot")
    print("2. Delete a working time slot")
    choice = int(input("\nEnter your choice: "))
    
    if choice == 1:
        username = session["username"]
        camp = session["camp_id"]
        day_of_week = input("\nEnter day of the week: ")
        start_time = input("Enter start time: ")
        end_time = input("Enter end time: ")

        scheduling_system.add_availability(username, camp, day_of_week, start_time, end_time)

    elif choice == 2:
        username = session["username"]
        camp = session["camp_id"]
        day_of_week = input("\nEnter day of the week: ")
        start_time = input("Enter start time: ")
        end_time = input("Enter end time: ")

        scheduling_system.delete_availability(username, camp, day_of_week, start_time, end_time)


