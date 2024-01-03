# start here
from connectdb import setup_conn, setup_db, view_table
from populatedb import *
from fs import hash_password
from user import *
import fcamp
from hpava import HumanitarianPlan
import os
# from resources import input_ressources_old
from loggs_system import UserAuthenticationSystem

authentication_system = UserAuthenticationSystem()

def start_main():
    import install_libraries
    setup_conn()
    setup_db()
    pop_db()

    print("\n------WELCOME TO THE MAIN MENU------\n")
    while True:
        from optionsmenu import main_menu
        choice = main_menu()

        if choice == "1":
            login_function()

        elif choice == "0":
            print("\nExiting program.")
            quit()

        else:
            print("\nInvalid choice.")


def login_function():
    print("\n------LOG IN------")
    while True:
        logintype = input("\nDo you want to log in as an admin or as a volunteer? (admin/volunteer, press 0 to exit): ")

        if logintype == "admin":
                
                while True:
                    username = input("\nEnter your username (enter 0 to exit): ")

                    if username == 'admin':
                        while True:
                            password = input("\nEnter your password (enter 0 to exit): ")

                            if password == '111':
                                authentication_system.log_in(username)
                                print("\nSuccessful Loggin!")
                                session = {
                                            'username': 'admin',
                                            'name': 'admin',
                                            'surname': 'admin',
                                            'phone': '123456789',
                                            'camp_id': 1,
                                            'availability': 'available',
                                            'user_type': 'admin',
                                            'status': 'active'
                                        }
                                from optionsmenu import admin_menu
                                admin_menu(session)

                            elif password == '0':
                                print('\nExiting...')
                                break

                            else:
                                print("\nInvalid password.")

                    elif username == '0':
                        print('\nExiting...')
                        break
                    
                    else:
                        print("\nInvalid username.")

        elif logintype == "volunteer":
            user = None  # Initialize user outside the loop

            while True:
                if logintype == "volunteer":
                    username = input("\nEnter your username (enter 0 to exit): ")

                    if username == '0':
                        break

                    else:
                        with setup_conn() as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
                            result = cursor.fetchone()

                            if result is not None and result[0] == username:    
                                cursor.execute("SELECT status FROM users WHERE username = ?", (username,))
                                result = cursor.fetchone()

                                if result[0] == 'active':
                                    password = input("\nEnter your password (enter 0 to exit): ")

                                    if password == '111':
                                        authentication_system.log_in(username)
                                        print("\nSuccessful Loggin!")


                                    elif password == '0':
                                        print('\nExiting...')
                                        break

                                    else:
                                        print("\nIncorrect password")

                                    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                                    user_data = cursor.fetchone()
                                    

                                    if user_data:
                                        session = create_user_session({
                                            'userID': user_data[0],
                                            'username': user_data[1],
                                            'name': user_data[3],
                                            'surname': user_data[4],
                                            'phone': user_data[5],
                                            'camp_id': user_data[6],
                                            'availability': user_data[7],
                                            'user_type': user_data[8],
                                            'status': user_data[9]
                                        })

                                    from optionsmenu import volunteer_menu
                                    volunteer_menu(session)

                                elif result[0] == 'inactive':
                                    print("\nThe account has been deactivated, please contact the administrator.")

                                # Rest of your code...

                                elif username == '0':
                                    print('\nExiting...')
                                    break

                                else:
                                    print("\nIncorrect username")
                            else:
                                print("\nInvalid username. Please try again.")


        elif logintype == '0':
            print('Exiting...')
            break

        else:
            print("Invalid user type. Please try again.")


def create_user_session(user_data):
    session = {
        'userID': user_data['userID'], 
        'username': user_data['username'],
        'name': user_data['name'],
        'surname': user_data['surname'],
        'phone': user_data['phone'],
        'camp_id': user_data['camp_id'],
        'availability': user_data['availability'],
        'user_type': user_data['user_type'],
        'status': user_data['status']
    }
    return session

if __name__ == '__main__':
    start_main()

