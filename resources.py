from connectdb import setup_conn, update_table, select_item
from datetime import datetime


class RessourcesOld:

    def __init__(self, camp_id: int, volunteer_id: int, entry_date: str, gluten_free: int,
                 dairy_free: int, no_nuts: int, vegan: int, vegetarian: int, omnivore: int,
                 epipen: int, pain_relief: int, bandages: int):
        self.campID = camp_id
        self.volunteerID = volunteer_id
        self.entryDate = entry_date
        self.glutenFree = gluten_free
        self.dairyFree = dairy_free
        self.noNuts = no_nuts
        self.vegan = vegan
        self.vegetarian = vegetarian
        self.omnivore = omnivore
        self.epipen = epipen
        self.painRelief = pain_relief
        self.bandages = bandages

    def edit_ressources_old(self):
        with setup_conn() as conn:
            cursor = conn.cursor()
            data = (self.campID, self.volunteerID, self.entryDate, self.glutenFree, self.dairyFree, self.noNuts,
                    self.vegan, self.vegetarian, self.omnivore, self.epipen, self.painRelief, self.bandages)
            update_table(cursor, 'ressourcesOld', data)




class RessourcesNew():

    def __init__(self, humanitarian_plan: int, camp_id: int, new_gluten_free: int, new_dairy_free: int,
                 new_no_nuts: int, new_vegan: int, new_vegetarian: int, new_omnivore: int,
                 new_epipen: int, new_pain_relief: int, new_bandages: int):
        self.humanitarianplan = humanitarian_plan
        self.campID = camp_id
        self.newGF = new_gluten_free
        self.newDairyFree = new_dairy_free
        self.newNoNuts = new_no_nuts
        self.newVegan = new_vegan
        self.newVegetarian = new_vegetarian
        self.newOmnivore = new_omnivore
        self.newEpipen = new_epipen
        self.newPainRelief = new_pain_relief
        self.newBandages = new_bandages

    def edit_ressources_new(self):
        with setup_conn() as conn:
            cursor = conn.cursor()
            data = (
            self.humanitarianplan, self.campID, self.newGF, self.newDairyFree, self.newDairyFree, self.newNoNuts,
            self.newVegan, self.newVegetarian, self.newOmnivore, self.newEpipen, self.newPainRelief, self.newBandages)
            update_table(cursor, 'ressourcesNew', data)


def new_resources_old():
        with setup_conn() as conn:
            cursor = conn.cursor()
            query = """SELECT c.campID FROM camps c WHERE NOT EXISTS (SELECT campID FROM ressourcesOld r WHERE r.campID = c.campID)"""
            cursor.execute(query)
            missing_camp_id = cursor.fetchone()
            capacity_query = """SELECT capacity FROM camps WHERE campID = ?"""
            cursor.execute(capacity_query, (missing_camp_id[0],))
            capacity = cursor.fetchone()
            capacity_fill = capacity[0]*7
            data = (missing_camp_id,) + tuple(capacity_fill for _ in range(15))
            update_table(cursor, 'ressourcesOld', data)
            conn.commit()


def input_ressources_old():
    print("Welcome to the Ressources log!")
    # for now as I dont have authentication
    camp_id = input("Enter the camp ID: ")
    volunteer_id = input("Enter your volunteer ID: ")

    input_entry_date = datetime.now().strftime("%d-%m-%y")
    input_gluten_free = input("Enter the number of gluten free items available: ")
    input_dairy_free = input("Enter the number of dairy free items available: ")
    input_no_nuts = input("Enter the number of nut free items available: ")
    input_vegan = input("Enter the number of vegan items available: ")
    input_vegetarian = input("Enter the number of vegetarian items available: ")
    input_omnivore = input("Enter the number of food items not fitting the previous description: ")
    input_epipen = input("Enter the number of Epipens available: ")
    input_pain_relief = input("Enter the number of pain relief medicine available: ")
    input_bandages = input("Enter the number of bandages available: ")

    update_ressources_old = RessourcesOld(camp_id, volunteer_id, input_entry_date, input_gluten_free,
                                          input_dairy_free, input_no_nuts, input_vegan, input_vegetarian,
                                          input_omnivore, input_epipen, input_pain_relief, input_bandages)

    return RessourcesOld(camp_id, volunteer_id, input_entry_date, input_gluten_free,
                         input_dairy_free, input_no_nuts, input_vegan, input_vegetarian,
                         input_omnivore, input_epipen, input_pain_relief, input_bandages)


def ressources_left_week():
    print("Welcome to the overview of the ressources left!")
    camp_check = input("Please input the  camp ID: ")
    where = 'campID'
    items_left_list = ['glutenFree', 'dairyFree', 'noNuts', 'vegan', 'vegetarian', 'omnivore',
                       'epipen', 'painRelief', 'bandages']
    item_left_nb = []
    for item in items_left_list:
        result_items = select_item(item, 'ressourcesOld', where, camp_check)
        if result_items:
            quantity_items = result_items[0]
            quantity_per_week = quantity_items / 7
            item_left_nb.append((item, quantity_per_week))
        else:
            print(f"Item '{item}' not found in the 'ressourcesOld' table.")
    for item, quantity_per_week in item_left_nb:
        print(f"Item: {item}, Quantity left per week: {quantity_per_week: .2f}")


def new_resources_new():
        with setup_conn() as conn:
            cursor = conn.cursor()
            query = """SELECT h.planID FROM humanitarianplan h WHERE NOT EXISTS (SELECT planID FROM ressourcesNew r WHERE r.planID = h.planID)"""
            cursor.execute(query)
            missing_plan_id = cursor.fetchone()
            data = (missing_plan_id,) + tuple(50 for _ in range(14))
            update_table(cursor, 'ressourcesNew', data)
            conn.commit()

