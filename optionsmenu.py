# for presenting the user with options
from refugee import *
from hpava import *
from hpava import HumanitarianPlan
from fcamp import *
from schedulling_system import *

from loggs_system import UserAuthenticationSystem

authentication_system = UserAuthenticationSystem()

###### main menu
def main_volunteer_management():
    print("\nVolunteer Managment Menu:")
    print("1. Create New Volunteer")
    print("2. Edit Volunteer Info")
    print("3. View All Volunteers")
    print("4. View Vounteers Avalability Table")
    print("0. Exit")
    return int(input("Choose an option: "))


####### AVA
def menu_humanitarian_plan():
    print("\n-------------------Humanitarian Plan Menu---------------------")
    print("1. Create new humanitarian plan")
    print("2. View all humanitarian plans")
    print("3. View a specific humanitarian plan")
    print("4. Edit humanitarian plan")
    print("5. Delete humanitarian plan")
    print("6. Close humanitarian plan")
    print("0. Exit")
    return int(input("Choose an option: "))


#### CATH
def menu_edit_humanitarian_plan():
    print("\nOptions to edit")
    print("1. Type")
    print("2. Description")
    print("3. Location")
    print("4. Start Date")
    print("0. Exit")
    return int(input("Choose an attribute to edit: "))


def menu_ressources():
    print("\nRessources Management Menu: ")
    print("1. Input New Ressources")
    print("2. View Ressources")
    print("0. Exit")
    return int(input("Choose an option: "))


def main_menu():
    print("1. Log in")
    print("0. Exit")
    return input("\nChoose an option: ")


def admin_menu_pcr():
    print("\nManage emergency plans, camps and resource: ")
    print("1. Manage emergency plans")
    print("2. Manage camps")
    print("3. Manage resources")
    print("0. Exit")
    return int(input("Choose an option: "))

def volunteer_menu_RCR():
    print("\nWhat would you like to do?")
    print("1. Manage refugees")
    print("2. View your camp info")
    print("3. Manage resources")
    print("0. Exit")
    return int(input("Choose an option: "))   

def menu_options_camp(): # seperate add camp
    print("\nCamp Managment Menu:")
    print("1. Create New Camp")
    print("2. View All Camps")
    print("3. View a specific camp")
    print("4. Delete A Camp")
    print("5. Activate/deactivate a camp")
    print("0. Exit")
    return int(input("\nChoose an option: "))

'''
def ressourcers_menu():
    setup_db()

    while True:
        choice = optionsmenu.menu_ressources()
        match choice:
            case 1:
                new_inventory = input_ressources_old()
                new_inventory.edit_ressources_old()
                print("Ressources updated!")
            case 2:
                view_table('ressourcesOld')
            case 0:
                print("Exiting program.")
                break
            case _:
                print("Invalid option. Please try again.")
'''


def add_more_c_menu():
    print("\nDo u want to add more camps now?")
    print("1. Yes")
    print("0. No")
    return int(input("\nChoose an option: "))


def add_v_r_menu():
    print("\nDo u want to add volunteers or refugees now?")
    print("1. Yes")
    print("0. No")
    return int(input("\nChoose an option: "))


def add_v_r_options():
    print("\nWould you like to add any more refugees or volunteers?")
    print('1. Yes, refugees')
    print('2. Yes, volunteer')
    print('0. Exit')
    return int(input("\nChoose an option: "))

def schedulling_menu():
    print('\nWhat would you like to do?')
    print("1. View my schedule")
    print("2. View overall schedule")
    print("3. Edit my availability")
    print("0. Exit")

    choice = int(input("\nEnter your choice: "))

    return choice


###### admin menu 
def admin_menu(session):
    from user import Admin
    while True:
        print("\n--- Admin Menu ---")
        print("1. Admin info")
        print("2. Manage volunteers")
        print("3. Manage emergency plans, camps and resources")
        print("0. Logout")

        while True:
            admin_choice = input("\nEnter your choice: ")

            try:
                admin_choice = int(admin_choice)
                break

            except:
                print("Invalid input, please try again.")

        if admin_choice == 1:
            Admin.__str__(session)
        
        elif admin_choice == 2:
            while True:
                choice = main_volunteer_management()

                if choice == 1:
                    Admin.create_volunteer()
                
                elif choice == 2:
                    Admin.edit_user_information(session)

                elif choice == 3:
                    view_table('users')

                elif choice == 4:
                    view_table('availability')

                elif choice == 0:
                    admin_menu(session)

                else:
                    print("\nInvalid choice.")


        elif admin_choice == 3:
            while True:
                chosen_choice = admin_menu_pcr()

                if chosen_choice == 1:
                    hp_menu(session) 

                elif chosen_choice == 2:
                    camp_menu(session) 

                elif chosen_choice == 3:
                    #resources_menu() 
                    pass

                elif chosen_choice == 0:
                    admin_menu(session)

                else:
                    print("\nInvalid choice.")        

        elif admin_choice == 0:
            from main import start_main
            authentication_system.log_out(session["username"])
            start_main()

        else:
            print("\nInvalid choice.")


###### volunteer menu
def volunteer_menu(session):
    from user import Volunteer
    while True:
        print("\n--- Volunteer Menu ---")
        print("1. Volunteer info")
        print("2. Edit volunteer info") 
        print("3. Manage refugees, camps and resources")
        print("4. Manage schedule")
        print("0. Logout")

        while True:
            volunteer_choice = input("\nEnter your choice: ")

            try:
                volunteer_choice = int(volunteer_choice)
                break

            except:
                print("Invalid input, please try again.")

        if volunteer_choice == 1:
            Volunteer.__str__(session)  # showing volunteer's personal info

        elif volunteer_choice == 2:
            Volunteer.edit_user_information(session)

        elif volunteer_choice == 3:
            while True:
                choice = volunteer_menu_RCR()

                if choice == 1:
                    refugee_menu(session)

                elif choice == 2:
                    view_table('camps')

                elif choice == 0:
                    volunteer_menu(session)

                else:
                    print("\nInvalid choice.") 

        elif volunteer_choice == 4:
            while True:
                choice = schedulling_menu()

                if choice == 1:
                    scheduling_system.get_availability(session)

                elif choice == 2:
                    view_table('availability')

                elif choice == 3:
                    edit_availability(session)
                    
                elif choice == 0:
                    volunteer_menu(session)

                else:
                    print("\nInvalid choice.") 

        elif volunteer_choice == 0:
            from main import start_main
            authentication_system.log_out(session["username"])
            start_main() 

        else:
            print("\nInvalid choice.")


def refugee_menu(session):
    while True:
        print("\n--- Refugee Menu ---")
        print("1. Create refugee record")
        print("2. View refugee record")
        print("3. Search refugee record")
        print("4. Remove refugee record")
        print("0. Back to Volunteer Menu")

        while True:
            volunteer_choice = input("\nEnter your choice: ")

            try:
                volunteer_choice = int(volunteer_choice)
                break

            except:
                print("Invalid input, please try again.")

        if volunteer_choice == 1:
            Refugee.create_refugee_menu()

        elif volunteer_choice == 2:
            Refugee.view_refugee()

        elif volunteer_choice == 3:
            Refugee.search_refugee()

        elif volunteer_choice == 4:
            Refugee.delete_refugee_menu()

        elif volunteer_choice == 0:
            volunteer_menu(session)

        else:
            print("\nInvalid choice.")


# these three are for the admin
def hp_menu(session):
    choice_hp = menu_humanitarian_plan()
    match choice_hp:
        case 1:
            newplan = HumanitarianPlan.create_humanitarian_plan_menu()
            HumanitarianPlan.create_humanitarian_plan(newplan)
            last_hp_id = get_id_from_db()
            while True: 
                new_camp = create_camp_input_hp(last_hp_id)
                new_camp.create_camp()
                add_vr = add_v_r_menu() # possibility to add volunteers and refugees while creating a plan-camp
                if add_vr == 1:
                    while True:
                        print('\nAdd refugees') 
                        Refugee.create_refugee_menu()
                        print('\nAdd vounteer')
                        from user import Admin
                        Admin.create_volunteer()
                        add_more_r_v = add_v_r_options()
                        if add_more_r_v == 0:
                            break
                add_more_camps = add_more_c_menu()
                if add_more_camps != 1:
                    break         
        case 2:
            view_table('humanitarianplan')
            menu_humanitarian_plan()
            
        case 3:
            # view specific table
            planID = int(input("\nEnter the planID which you want to view:"))
            view_specific_row(planID, 'humanitarianplan')

        case 4:
            input_plan_id = int(input("\nEnter the planID which you want to edit:"))
            HumanitarianPlan.edit_humanitarian_plan(input_plan_id)
            HumanitarianPlan.edit_humanitarian_plan_menu(input_plan_id)
            menu_humanitarian_plan()
    while True:
        while True:
            choice_hp = menu_humanitarian_plan()

            try:
                choice_hp = int(choice_hp)
                break

            except:
                print("Invalid input, please try again.")

        match choice_hp:
            case 1:
                newplan = HumanitarianPlan.create_humanitarian_plan_menu()
                HumanitarianPlan.create_humanitarian_plan(newplan)
                last_hp_id = get_id_from_db()
                while True: 
                    new_camp = create_camp_input_hp(last_hp_id)
                    new_camp.create_camp()
                    add_vr = add_v_r_menu() # possibility to add volunteers and refugees while creating a plan-camp
                    if add_vr == 1:
                        while True:
                            print('\nAdd refugees') 
                            Refugee.create_refugee_menu()
                            print('\nAdd vounteer')
                            from user import Admin
                            Admin.create_volunteer()
                            add_more_r_v = add_v_r_options()
                            if add_more_r_v == 0:
                                break
                    add_more_camps = add_more_c_menu()
                    if add_more_camps != 1:
                        break         
            case 2:
                view_table('humanitarianplan')
                menu_humanitarian_plan()

            case 3:
                input_plan_id = int(input("\nEnter the planID which you want to edit: "))
                HumanitarianPlan.edit_humanitarian_plan_menu(input_plan_id)
                menu_humanitarian_plan()

        case 5:
            deletedplan = HumanitarianPlan.delete_humanitarian_plan_menu()
            HumanitarianPlan.delete_humanitarian_plan(deletedplan)
            delete_camp_by_hp(deletedplan)
            menu_humanitarian_plan()
            case 4:
                deletedplan = HumanitarianPlan.delete_humanitarian_plan_menu()
                HumanitarianPlan.delete_humanitarian_plan(deletedplan)
                menu_humanitarian_plan()

        case 6:
            end_date, input_plan_id = HumanitarianPlan.close_humanitarian_plan_menu()
            HumanitarianPlan.close_humanitarian_plan(end_date, input_plan_id)
            # TO THINK
            # what to do with camps when plan is closed?
            # delete_camp_by_hp(input_plan_id)
            menu_humanitarian_plan()
            case 5:
                end_date, input_plan_id = HumanitarianPlan.close_humanitarian_plan_menu()
                HumanitarianPlan.close_humanitarian_plan(end_date, input_plan_id)
                # TO THINK
                # what to do with camps when plan is closed?
                # delete_camp_by_hp(input_plan_id)
                menu_humanitarian_plan()

            case 0:
                print("\nExiting program.")
                admin_menu(session)

            case _:
                print("\nInvalid choice.")


def camp_menu(session):
    while True:
        while True:
            choice_camp = menu_humanitarian_plan()

            try:
                choice_camp = int(choice_camp)
                break

            except:
                print("Invalid input, please try again.")
        
        match choice_camp:
            case 1:
                new_camp = create_camp_input()
                new_camp.create_camp()
                print("\nCamp added successfully.")

        case 2:
            print("\n------VIEWING CAMPS------")
            view_table('camps')
        
        case 3:
            # view specific table
            campID = int(input("\nEnter the campID which you want to view:"))
            view_specific_row(campID, 'camps')

        case 4:
            transfer_or_delete_people()
            
        case 5:
            what = int(input("\nWhat do you want to do, activate [1] or deactivate? [2]: "))
            if what == 1:
                newstatus = 'Active'
            case 2:
                print("\n------VIEWING CAMPS------")
                view_table('camps')

            case 3:
                transfer_or_delete_people()
                
            case 4:
                what = int(input("\nWhat do you want to do, activate [1] or deactivate? [2]: "))
                if what == 1:
                    newstatus = 'Active'

                else:
                    newstatus = 'Inactive'
                update_camp_status(newstatus)
                # MAJA rethink if we need this

            case 0:
                print("\nExiting program.")
                admin_menu(session)

            case _:
                print("\nInvalid choice.")
        
    