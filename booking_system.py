from connectdb import get_volunteer_id, get_timeslot_id, get_refugee_id, is_available, insert_query, setup_conn
from datetime import datetime




def menu_booking():
    print("Hello to the booking system")
    refugee = input("Please input the refugee's full name: ")
    refugee_id = get_refugee_id(refugee)
    
    #book by name or book by username
    search_style = input("Do you know the name or username?\nIf name select 1 and if username select 2: ")
    if search_style == '1':
        name = input("What is the name of the volunteer: ")
        volunteer_id = get_volunteer_id(name, '1')
        
    elif search_style == '2':
        username = input("what is the username of the volunteer: ")
        volunteer_id = get_volunteer_id(username, '2')
        
    else:
        print("ERROR: PLEASE SELECT AN OPTION AVAILABLE")
    
    day_input = input("Which day would you like to book\n[1] Monday [2] Tuesday [3] Wednesday [4] Thursday [5] Friday: ")
    days = {
        '1':'Monday',
        '2':'Tuesday',
        '3':'Wednesday',
        '4':'Thursday',
        '5':'Friday'
    }
    if day_input not in days:
        "Invalid day input"
    day = days[day_input]

    time = input("What time would you like to book the meeting for? (format: hh:mm:ss)")
    timeslot_id = get_timeslot_id(day,time)
    print(timeslot_id)
    #check if available
    availibility = is_available(timeslot_id[0], volunteer_id[0])
    if availibility == 0:
        status = "Confirmed"
        entryDate = datetime.now().strftime("%d-%m-%y")
        booking_data = (volunteer_id[0], timeslot_id[0], refugee_id[0], entryDate, status)
        print(booking_data)
        with setup_conn() as conn:
            cursor = conn.cursor()
            insert_query(cursor, 'booking', booking_data)
        print("Booking succesfully created")
    else:
        print("Booking cannot be made due to inavailability")

menu_booking()








    #have them input and then look thorugh system for that volunteer
    #ask for time and day and check for coincidings

#create booking table
menu_booking()