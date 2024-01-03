from connectdb import setup_conn, insert_query, remove_query1
from fs import hash_password
from optionsmenu import admin_menu, volunteer_menu

class User:
    def __init__(self, username: str, password: str, name: str, surname: str, phone: str, user_type, status="active"):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.phone = phone
        self.user_type = user_type
        self.status = status

    @staticmethod
    def __str__(session):
        while True:
            print("\n--- " + session['user_type'] + " Info ---")
            print("Username: " + session['username'])
            print("First name: " + session['name'])
            print("Last name: " + session['surname'])
            print("Phone number: ",  session['phone'])
            print("Camp ID: ",  session['camp_id'])
            print("Status: " + session['status'])
            if session['user_type'] == "volunteer":
                print("Availability: " + session['availability'])
            else:
                pass

            if session['user_type'] == "admin":
                admin_menu(session)
                
            elif session['user_type'] == "volunteer":
                volunteer_menu(session)

    @staticmethod
    def edit_user_information(session):
        print(f"\n--- LOGGED IN AS: {session['username']} ---")
        while True:
            if session["user_type"] == 'admin':
                print("\nWould you like to change users 1. account status or 2. other? ")
                print("1. Status")
                print("2. Other")

                while True:
                    choice = int(input("\nEnter you choice: "))

                    try:
                        choice = int(choice)
                        break

                    except:
                        print("Invalid input, please try again.")

                username = input("\nEnter the username of the volunteer to be edited: ")

                if choice == 1:
                    print("\nWould you like to deactivate, reactivate or delete the account? ")
                    print("1. Deactivate")
                    print("2. Reactivate")
                    print("3. Delete")

                    while True:
                        choice = int(input("\nEnter you choice: "))

                        try:
                            choice = int(choice)
                            break

                        except:
                            print("Invalid input, please try again.")

                    if choice == 1:
                        Admin.deactivate_volunteer(username)
                        admin_menu(session)

                    elif choice == 2:
                        Admin.reactivate_volunteer(username)
                        admin_menu(session)

                    elif choice == 3:
                        Admin.delete_volunteer(username)
                        admin_menu(session)

                    else:
                        print("Invalid choice, try again")

                elif choice == 2:

                    with setup_conn() as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
                        result = cursor.fetchone()
                    
                    if result is not None:
                        username_found = result[0]
                        print(f"Username '{username_found}' exists.")
                    
                    else:
                        print(f"Username '{username}' or account does not exist.")
                        continue
                
                attribute_mapping = {
                            1: ("username", f"{username}'s username"),
                            2: ("name", f"{username}'s name"),
                            3: ("surname", f"{username}'s surname"),
                            4: ("phone", f"{username}'s phone"),
                            5: ("camp_id", f"{username}'s camp id")
                        }
                
                while True:
                    print("\n--- What volunteer's personal information would you like to edit? ---")
                    for key, value in attribute_mapping.items():
                        print(f"{key}. {value[1]}")

                    print("6. Exit to user menu")

                    while True:
                        choice = int(input("\nEnter you choice: "))

                        try:
                            choice = int(choice)
                            break

                        except:
                            print("Invalid input, please try again.")

                    if choice == '6':
                        print("\nExiting...")
                        admin_menu(session)

                    try:
                        choice = int(choice)

                    except ValueError:
                        print("\nInvalid choice. Please enter a number.")
                        continue

                    if choice in attribute_mapping:
                        attribute_name, prompt = attribute_mapping[choice]

                        with setup_conn() as conn:
                            cursor = conn.cursor()
                            query = f"SELECT {attribute_name} FROM users WHERE username = ?"
                            cursor.execute(query, (username,))
                            result = cursor.fetchone()

                        current_value = result[0]
                        entered_value = input(f"\nEnter {prompt} again: ")

                        if attribute_name == 'phone' or attribute_name == 'camp_id':
                            entered_value = int(entered_value)

                        if current_value == entered_value:
                            new_value = input(f"\nEnter new {prompt}: ")

                            try:
                                with setup_conn() as conn:
                                    cursor = conn.cursor()
                                    query = f"UPDATE users SET {attribute_name} = ? WHERE username = ?"
                                    cursor.execute(query, (new_value, username,))
                                    conn.commit()
                            
                                print(f"{username}'s information has been updated")

                            except Exception as e:
                                print(f"Error: {e}")
                                conn.rollback()
                            finally:
                                conn.close()

                        else:
                            print(f"\nIncorrect {attribute_name}")
            
                    else:
                        print("\nInvalid choice. Please enter a number between 1 and 6.")

#########################

            elif session["user_type"] == "volunteer":
                attribute_mapping = {
                1: ("username", f"{session['username']}'s username"),
                2: ("name", f"{session['username']}'s name"),
                3: ("surname", f"{session['username']}'s surname"),
                4: ("phone", f"{session['username']}'s phone")
            }
                    
                while True:
                    print("\n--- What personal information would you like to edit? ---")
                    for key, value in attribute_mapping.items():
                        print(f"{key}. {value[1]}")

                    print("6. Exit to user menu")

                    choice = input("\nEnter your choice: ")

                    if choice == '6':
                        print("\nExiting...")
                        volunteer_menu(session)

                    try:
                        choice = int(choice)
                    except ValueError:
                        print("\nInvalid choice. Please enter a number.")
                        continue

                    if choice in attribute_mapping:
                        attribute_name, prompt = attribute_mapping[choice]

                        with setup_conn() as conn:
                            cursor = conn.cursor()
                            query = f"SELECT {attribute_name} FROM users WHERE username = ?"
                            cursor.execute(query, (session['username'],))
                            result = cursor.fetchone()

                        current_value = result[0]
                        entered_value = input(f"\nEnter {prompt} again: ")

                        if attribute_name == 'phone' or attribute_name == 'camp_id':
                            entered_value = int(entered_value)

                        if current_value == entered_value:
                            new_value = input(f"\nEnter new {prompt}: ")

                            try:
                                with setup_conn() as conn:
                                    cursor = conn.cursor()
                                    query = f"UPDATE users SET {attribute_name} = ? WHERE username = ?"
                                    cursor.execute(query, (new_value, session['username'],))
                                    conn.commit()
                            
                                print(f"\n{session['username']}'s information has been updated")

                            except Exception as e:
                                print(f"Error: {e}")
                                conn.rollback()
                            finally:
                                conn.close()

                        else:
                            print(f"\nIncorrect {attribute_name}")
            
                    else:
                        print("\nInvalid choice. Please enter a number between 1 and 6.")



class Admin(User):
    def __init__(self, username: str, password: str, name: str, surname: str, phone: str, user_type = "Admin", status="active"):
        super().__init__(username, password, name, surname, phone, user_type, status)

    @staticmethod
    def create_volunteer():
        print("\n------CREATING A NEW VOLUNTEER ACCOUNT------\n")
        input_username = input("Enter volunteer username: ")
        input_password = int(input("Enter volunteer password: "))
        # input_password = hash_password(input_password)
        input_name = input("Enter volunteer name: ")
        input_surname = input("Enter volunteer surname: ")
        input_phone = int(input("Enter volunteer phone: "))
        input_camp_id = int(input("Enter volunteer camp id: "))   
        input_availability = str(input("Enter volunteer availability: "))  

        volunteer = Volunteer(input_username, input_password, input_name, input_surname, input_phone, input_camp_id, input_availability)

        with setup_conn() as conn:
            cursor = conn.cursor()
            insert_query(cursor, 'users', volunteer)
            conn.commit()

        print("\n A new volunteer account has been successfully created.")

    @staticmethod
    def delete_volunteer(username):
        # check if user exists before deleing
        with setup_conn() as conn:
            cursor = conn.cursor()
            query = f"SELECT username FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

        if result is not None:
            print("The user does not exist.")
        
        else:
            # delete if user does exist
            with setup_conn() as conn:
                cursor = conn.cursor()
                remove_query1(cursor, 'users', username)
            conn.close()

            print(f"\nVolunteer {username} has been deleted")

    @staticmethod
    def deactivate_volunteer(username): 
        # check if the user has already been deactivatedd
        with setup_conn() as conn:
            cursor = conn.cursor()
            query = f"SELECT status FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

        if result is None:
            print("The user does not exist.")

        elif result[0] == 'inactive':
            print("The user is already inactive.")

        else:
            # inactvate if the user s still active
            with setup_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET status = ? WHERE username = ?", ("inactive",username,))
            conn.close()

            print(f"\nVolunteer {username} has been deactivated")

    def reactivate_volunteer(username):
        # check if the user has already been deactivatedd
        with setup_conn() as conn:
            cursor = conn.cursor()
            query = f"SELECT status FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

        if result is None:
            print("The user does not exist.")

        elif result[0] == 'active':
            print("The user is already active.")

        else:
            # if inactive then reactivate
            with setup_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET status = ? WHERE username = ?", ("active", username,))
            conn.close()
            
            print(f"\nVolunteer {username} has been reactivated")
            


class Volunteer(User):
    def __init__(self, username: str, password: str, name: str, surname: str, phone: int, camp_id: int, availability: str, user_type = "volunteer", status="active"):
        super().__init__(username, password, name, surname, phone, user_type, status)

        self.camp_id = camp_id
        self.availability = availability

'''connectdb.cursor.execute("SELECT * FROM volunteers")
print(connectdb.cursor.fetchall())'''
