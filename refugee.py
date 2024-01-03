from connectdb import *
from refugee_errorhandling import *
from fs import *


# Class Refugee contains all refugee-related functions e.g. create, remove, view and search etc.
class Refugee:
    # refugeeId set to None in the initialization here, for the actual value is an auto_incremented INT value determined
    # by the sqlite database.
    def __init__(self, name: str, surname: str, campId: str, age: str, languages: str, gender: str,
                 bloodType: str, psyHealth: str, physHealth: str, familyID: str, gluten_free: bool,
                 dairy_free: bool, no_nuts: bool, vegan: bool, vegetarian: bool, omnivore: bool,
                 epipen: bool, pain_relief: bool, bandages: bool, sanitaryProducts: bool, refugeeId=None):
        ##ERROR HANDLING ONLY ONE DIETARY REQUIREMENT CAN BE SELECTED
        self.name = name
        self.surname = surname
        self.campId = campId
        self.age = age
        self.languages = languages
        self.gender = gender
        self.bloodType = bloodType
        self.psyHealth = psyHealth
        self.physHealth = physHealth
        self.familyID = familyID
        self.glutenFree = gluten_free
        self.dairyFree = dairy_free
        self.noNuts = no_nuts
        self.vegan = vegan
        self.vegetarian = vegetarian
        self.omnivore = omnivore
        self.epipen = epipen
        self.painRelief = pain_relief
        self.bandages = bandages
        self.sanitaryProducts = sanitaryProducts
        self.refugeeId = refugeeId

    @staticmethod
    def create_refugee_menu():
        print("Welcome to the refugee menu")
        # Both name and surname can share the same error handling function at the moment
        inputName = alpha_input('name')
        inputSurname = alpha_input('surname')
        inputCampId = num_input('campId')
        inputAge = num_input('age')
        inputLan = alpha_input('language')
        inputGender = alpha_input('gender')
        inputBloodType = alpha_input('bloodType')
        inputPsyHealth = num_input('psyHealth')
        inputPhysHealth = num_input('physHealth')
        inputFamily = alpha_input('familyID')

        # Get boolean inputs
        inputGlutenFree = bool_input('Is the person gluten-free?')
        inputDairyFree = bool_input('Is the person dairy-free?')
        inputNoNuts = bool_input('Is the person allergic to nuts?')
        inputVegan = bool_input('Is the person vegan?')
        inputVegetarian = bool_input('Is the person vegetarian?')
        inputOmnivore = bool_input('Is the person an omnivore?')
        inputEpipen = bool_input('Does the person have an epipen?')
        inputPainRelief = bool_input('Does the person need pain relief?')
        inputBandages = bool_input('Does the person need bandages?')
        inputSanitaryProducts = bool_input('Does this person need sanitary products?')

        newRefugee = Refugee(inputName, inputSurname, inputCampId, inputAge, inputLan, inputGender, inputBloodType,
                             inputPsyHealth, inputPhysHealth, inputFamily, inputGlutenFree, inputDairyFree, inputNoNuts,
                             inputVegan, inputVegetarian, inputOmnivore, inputEpipen, inputPainRelief, inputBandages,
                             inputSanitaryProducts)

        Refugee.create_refugee(newRefugee)

        return newRefugee

    @staticmethod
    def delete_refugee_menu():
        print("\nWelcome to the delete refugee menu")
        inputID = input("\nEnter refugeeID: ")
        Refugee.delete_refugee(inputID)

    def create_refugee(newRefugee):
        with setup_conn() as conn:
            cursor = conn.cursor()
            query = "SELECT name, surname, campID, age, languages, gender, bloodType, psyHealth, physHealth, familyID, glutenFree, dairyFree, noNuts, vegan, vegetarian, omnivore, epipen, painRelief, bandages, sanitaryProducts FROM refugee WHERE name = ? AND surname = ? AND campID = ? AND age = ? AND languages = ? AND gender = ? AND bloodType = ? AND psyHealth = ? AND physHealth = ? AND familyID = ? AND glutenFree = ? AND dairyFree = ? AND noNuts = ? AND vegan = ? AND vegetarian = ? AND omnivore = ? AND epipen = ? AND painRelief = ? AND bandages = ? AND sanitaryProducts = ?"
            cursor.execute(query, (
                newRefugee.name, newRefugee.surname, newRefugee.campId, newRefugee.age,
                newRefugee.languages, newRefugee.gender, newRefugee.bloodType, newRefugee.psyHealth,
                newRefugee.physHealth, newRefugee.familyID, newRefugee.glutenFree, newRefugee.dairyFree,
                newRefugee.noNuts, newRefugee.vegan, newRefugee.vegetarian, newRefugee.omnivore,
                newRefugee.epipen, newRefugee.painRelief, newRefugee.bandages, newRefugee.sanitaryProducts
            ))
            result = cursor.fetchone()

        if result is None:
            with setup_conn() as connRef:
                cursor = connRef.cursor()
                result = insert_query(cursor, 'refugee', newRefugee)
                return result
            
        else:
            print("Refugee already exists.")

    @staticmethod
    def delete_refugee(refugeeId):
        with setup_conn() as conn:
            cursor = conn.cursor()
            query = f"SELECT refugeeID FROM refugee WHERE refugeeID = ?"
            cursor.execute(query, (refugeeId,))
            result = cursor.fetchone()

        if result is None:
            # print("\nThe refugee does not exist.")
            return 3

        else:
            with setup_conn() as connRef:
                cursor = connRef.cursor()
                result = remove_query2(cursor, 'refugee', 'refugeeID', int(refugeeId))
                if result:
                    # print(f"\nRefugee {refugeeId} has been removed.")
                    return 2
                else:
                    # print("\nRefugee removal failed.")
                    return 1

    def __str__(self):
        return (
            f"\n-------------------- Refugee Info --------------------\n"
            f"| {'Refugee ID:': <15} | {'First name:': <15} | {'Last name:': <15} | {'Camp ID:': <15} | "
            f"{'Age:': <15} | {'Languages:': <15} | {'Gender:': <15} | {'Blood type:': <15} | "
            f"{'Mental health:': <15} | {'Physical health:': <16} | {'Family ID:': <15}\n"

            # the refugee ID displayed now is the refugee name, will need to replace the data with actual ID read from
            # the table.
            f"| {self.refugeeId: <15} | {self.name: <15} | {self.surname: <15} | {self.campId: <15} | "
            f"{self.age: <15} | {self.languages: <15} | {self.gender: <15} | {self.bloodType: <15} | "
            f"{self.psyHealth: <15} | {self.physHealth: <16} | {self.familyID: <15}"
        )

    @staticmethod
    def view_refugee():
        with setup_conn() as connRef:
            cursor = connRef.cursor()
            view_table('refugee')
            # The order of elements SELECTED should be according to the initialization order of the python Refugee class
            # for the orders of elements between class and database are different.
            cursor.execute("SELECT name, surname, campID, age, languages, gender, bloodType, psyHealth, "
                           "physHealth, familyID, glutenFree, dairyFree, noNuts, vegan, vegetarian, "
                           "omnivore, epipen, painRelief, bandages, sanitaryProducts, refugeeId FROM refugee")
            return cursor.fetchall()
            '''for row in result:
                refugeeRecord = Refugee(*row)
                print(refugeeRecord)'''

            '''for row in cursor.fetchall():
                # Convert result retrieved from database back to Refugee class object to get access to the
                # __str__ function from the class to ensure output format.
                refugeeRecord = Refugee(*row)
                print(refugeeRecord)'''

    @staticmethod
    def search_refugee():
        # Use name + surname to avoid multiple possible outputs at this stage, should be combined with campId and family
        # to improve accuracy in later stages.
        while True:
            name = input("\nEnter refugee name: ")

            if isinstance(name, str):
                surname = input("\nEnter refugee surname: ")
                
                if isinstance(name, str):

                    with setup_conn() as conn:
                        cursor = conn.cursor()
                        query = f"SELECT name, surname FROM refugee WHERE name = ? AND surname = ?"
                        cursor.execute(query, (name, surname,))
                        result = cursor.fetchone()

                    if result is None:
                        print("The refugee does not exist.")
                        break

                    else:
                        with setup_conn() as connRef:
                            cursor = connRef.cursor()
                            cursor.execute("SELECT * FROM refugee WHERE name = ? AND surname = ?", (name, surname))
                            result = cursor.fetchall()

                            for row in result:
                                refugeeRecord = Refugee(*row)
                                print(refugeeRecord)

                            break

                else:
                    print("\nInvalid input. Please try again.")

            else:
                print("\nInvalid input. Please try again.")

    @staticmethod
    def edit_refugee_info():
        refugeeId = input("\nEnter ID to edit refugee info: ")
        with setup_conn() as conn:
                cursor = conn.cursor()
                query = f"SELECT id FROM refugee WHERE refugeeID = ?"
                cursor.execute(query, (refugeeId,))
                result = cursor.fetchone()

        if result is None:
            print("\nThe refugee does not exist.")

        else:
            with setup_conn() as connRef:
                cursor = connRef.cursor()
                cursor.execute("SELECT * FROM refugee WHERE refugeeID = ?", refugeeId)
                result = cursor.fetchall()
                refugeeRecord = None

                # This search is based on refugeeId so should have only one result
                for row in result:
                    refugeeRecord = Refugee(*row)
                    print(refugeeRecord)

                while True:
                ##ERROR HANDLING ONLY ONE DIETARY REQUIREMENT CAN BE SELECTED
                    print("Please select attribute you want to edit on: \n1. name\n2. surname\n3. campId\n4. age\n5. languages"
                        "\n6. gender\n7. blood type\n8. mental health\n9. physical health\n10. familyID\n11. gluten free\n12. dairy free"
                        "\n13. no nuts\n14. vegan\n15. vegetarian\n16. omnivore\n17. epipen\n18. pain relief\n19. bandages\n20. sanitary products\n0. Continue")
                    
                    user_choice = input("\nEnter your choice: ")

                    if user_choice == '1':
                        refugeeRecord.name = alpha_input('name')
                    elif user_choice == '2':
                        refugeeRecord.surname = alpha_input('surname')
                    elif user_choice == '3':
                        refugeeRecord.campId = num_input('campId')
                    elif user_choice == '4':
                        refugeeRecord.age = num_input('age')
                    elif user_choice == '5':
                        refugeeRecord.languages = input("Enter new refugee languages: ")
                    elif user_choice == '6':
                        refugeeRecord.gender = alpha_input('gender')
                    elif user_choice == '7':
                        refugeeRecord.bloodType = alpha_input('bloodType')
                    elif user_choice == '8':
                        refugeeRecord.psyHealth = num_input('psyHealth')
                    elif user_choice == '9':
                        refugeeRecord.physHealth = num_input('physHealth')
                    elif user_choice == '10':
                        refugeeRecord.familyID = alpha_input('familyID')
                    elif user_choice == '11':
                        refugeeRecord.glutenFree = bool_input('glutenFree')
                    elif user_choice == '12':
                        refugeeRecord.dairyFree = bool_input('dairyFree')
                    elif user_choice == '13':
                        refugeeRecord.noNuts = bool_input('noNuts')
                    elif user_choice == '14':
                        refugeeRecord.vegan = bool_input('vegan')
                    elif user_choice == '15':
                        refugeeRecord.vegetarian = bool_input('vegetarian')
                    elif user_choice == '16':
                        refugeeRecord.omnivore = bool_input('omnivore')
                    elif user_choice == '17':
                        refugeeRecord.epipen = bool_input('epipen')
                    elif user_choice == '18':
                        refugeeRecord.painRelief = bool_input('painRelief')
                    elif user_choice == '19':
                        refugeeRecord.bandages = bool_input('bandages')
                    elif user_choice == '20':
                        refugeeRecord.sanitaryProducts = bool_input('sanitaryProducts')
                    elif user_choice == '0':
                        break

                # Update database with new info
                if refugeeRecord:
                    sql = """
                    UPDATE refugee 
                    SET name = ?, surname = ?, campId = ?, age = ?, languages = ?, gender = ?, 
                    bloodType = ?, psyHealth = ?, physHealth = ?, familyID = ?, 
                    glutenFree = ?, dairyFree = ?, noNuts = ?, vegan = ?, vegetarian = ?, 
                    omnivore = ?, epipen = ?, painRelief = ?, bandages = ?, sanitaryProducts = ?
                    WHERE refugeeId = ?
                    """
                    cursor.execute(sql, (refugeeRecord.name, refugeeRecord.surname, refugeeRecord.campId,
                                refugeeRecord.age, refugeeRecord.languages, refugeeRecord.gender,
                                refugeeRecord.bloodType, refugeeRecord.psyHealth, refugeeRecord.physHealth,
                                refugeeRecord.familyID, refugeeRecord.glutenFree, refugeeRecord.dairyFree,
                                refugeeRecord.noNuts, refugeeRecord.vegan, refugeeRecord.vegetarian,
                                refugeeRecord.omnivore, refugeeRecord.epipen, refugeeRecord.painRelief,
                                refugeeRecord.bandages, refugeeRecord.sanitaryProducts,
                                refugeeId))
                    connRef.commit()

                    print("\nRefugee information edited")
                
                else:
                    print("\nError has occured.")
                


# '''
# ----------Hard coded function callings for testing purpose----------
# '''

# # this fraction is used to test consistent insert to the table.
# '''
# while True:
#     newRef = Refugee('john', 'doe', '1', '20', 'English', 'male', 'B', '8', '9', 'Doe')

#     with setup_conn() as connRef:
#         cursor = connRef.cursor()
#         insert_query(cursor, 'refugee', newRef)
# '''

# Refugee.create_refugee_menu()
# # Refugee.delete_refugee_menu()
# # Refugee.view_refugee()
# # Refugee.search_refugee()
# # Refugee.edit_refugee_info()
