# db connection and setup
import sqlite3
from datetime import datetime

 

def setup_conn():
    # establish connection
    return sqlite3.connect('database.db')


def setup_db():
    with setup_conn() as conn:
        cursor = conn.cursor()

        # create the humanitarian plan table - BY AVA
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS humanitarianplan (
                planID INTEGER PRIMARY KEY AUTOINCREMENT,
                type VARCHAR(15),
                description TEXT,
                location VARCHAR(30),
                campNo INTEGER,
                start_date TEXT,
                end_date TEXT)'''
        )

        #create the camp table  - finish the remaining attributes
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS camps (
                campID INTEGER PRIMARY KEY AUTOINCREMENT,
                planID INTEGER,
                country VARCHAR(50),
                city VARCHAR(50),
                capacity INTEGER,
                totalRefugees INTEGER,
                totalVolunteers INTEGER,
                status VARCHAR(10),
                resourcesState VARCHAR(15),
                totalGF INTEGER,
                totalDF INTEGER,
                totalNN INTEGER,
                totalVgn INTEGER,
                totalVgt INTEGER,
                totalOmn INTEGER,
                totalSP INTEGER,
                temperature INTEGER,
                humidity INTEGER,
                windSpeed INTEGER,
                weatherDescription VARCHAR(30),
                weather VARCHAR(50))'''
        )

        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users (
                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255),
                password VARCHAR(255),
                name VARCHAR(255),
                surname VARCHAR(255),
                phone INTEGER(15),
                campID INTEGER(15),
                availability VARCHAR(255),
                user_type VARCHAR(50),
                status VARCHAR(50))'''
        )

        cursor.execute(
        '''CREATE TABLE IF NOT EXISTS refugee (
            refugeeID INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            surname VARCHAR(255),
            campID INTEGER,
            age INTEGER,
            languages VARCHAR(255),
            gender VARCHAR(255),
            bloodType VARCHAR(255),
            psyHealth VARCHAR(255),
            physHealth VARCHAR(255),
            familyID INTEGER,
            glutenFree BOOLEAN,
            dairyFree BOOLEAN,
            noNuts BOOLEAN,
            vegan BOOLEAN,
            vegetarian BOOLEAN,
            omnivore BOOLEAN,
            epipen BOOLEAN,
            painRelief BOOLEAN,
            bandages BOOLEAN,
            sanitaryProducts BOOLEAN,
            FOREIGN KEY (campID) REFERENCES camps(campID) ON DELETE CASCADE ON UPDATE CASCADE)  
            '''
        )

        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS ressourcesOld (
                campID INTEGER,
                volunteerID INTEGER,
                entryDate DATE,
                glutenFree INTEGER,
                dairyFree INTEGER,
                noNuts INTEGER,
                vegan INTEGER,
                vegetarian INTEGER,
                omnivore INTEGER,
                epipen INTEGER,
                sanitaryProducts INTEGER,
                painRelief INTEGER,
                bandages INTEGER,
                coughsyrup INTEGER,
                allergyMedication INTEGER,
                indigestion INTEGER,
                skincream INTEGER,
                FOREIGN KEY (campID) REFERENCES humanitarianplan(campID) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (volunteerID) REFERENCES users(volunteerID) ON DELETE CASCADE ON UPDATE CASCADE)'''
        )

        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS ressourcesNew (
                planID INTEGER,
                newGF INTEGER,
                newDairyFree INTEGER,
                newNoNuts INTEGER,
                newVegan INTEGER,
                newVegetarian INTEGER,
                newOmnivore INTEGER,
                newEpipen INTEGER,
                newSanitaryProducts INTEGER,
                newPainRelief INTEGER,
                newBandages INTEGER,
                newCoughsyrup INTEGER,
                newAllergyMedication INTEGER,
                newIndigestion INTEGER,
                newSkincream INTEGER,
                FOREIGN KEY (planID) REFERENCES humanitarianplan(planID) ON DELETE CASCADE ON UPDATE CASCADE)'''
        )

        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS bookings (bookingID INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER,bookingDate DATE, FOREIGN KEY (userID) REFERENCES users(userID))'''
        )

def insert_query(cursor, table, thedata):
    match table:
        case 'camps':
            cursor.execute("INSERT INTO camps (planID, country, city, capacity, totalRefugees, totalVolunteers, status, resourcesState, totalGF, totalDF, totalNN, totalVgn, totalVgt, totalOmn, totalSP, temperature, humidity, windSpeed, weatherDescription, weather ) VALUES "
                           "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?)", thedata)

        case 'humanitarianplan':
            cursor.execute("INSERT INTO humanitarianplan (type, description, location, campNo, start_date) VALUES (?, ?, ?, ?, ?)", thedata)

        case 'users':
            cursor.execute("INSERT INTO users (username, password, name, surname, phone, campID, availability, user_type, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", thedata)

    # if table == 'users':
    #     data_tuple = (thedata.username, thedata.password, thedata.name, thedata.surname, thedata.phone, thedata.campID, thedata.availability, thedata.user_type, thedata.status)
    #     cursor.execute("INSERT INTO users (username, password, name, surname, phone, campID, availability, user_type, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data_tuple)


    if table == 'refugee':

        data_tuple = (thedata.name, thedata.surname, thedata.age, thedata.campId, thedata.languages, thedata.gender,

                      thedata.bloodType, thedata.psyHealth, thedata.physHealth, thedata.familyID, thedata.glutenFree,

                      thedata.dairyFree, thedata.noNuts, thedata.vegan, thedata.vegetarian, thedata.omnivore,

                      thedata.epipen, thedata.painRelief, thedata.bandages, thedata.sanitaryProducts)

        cursor.execute(
            "INSERT INTO refugee ('name', 'surname', 'age', 'campID', 'languages', 'gender', 'bloodType', 'psyHealth', "
            "'physHealth', 'familyID', 'glutenFree', 'dairyFree', 'noNuts', 'vegan', 'vegetarian', 'omnivore', 'epipen', 'painRelief', "
            "'bandages', 'sanitaryProducts') "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_tuple)
        if cursor.rowcount == 1:
            return True
        else:
            return False
        
    else:
        pass
        # raise error

def remove_query1(cursor, table, target):
    if table == 'users':
        cursor.execute("DELETE FROM users WHERE username = ?", (target,))

    elif table == 'refugee':
        cursor.execute("DELETE FROM refugee WHERE refugeeID = ?", (target,))
        if cursor.rowcount > 0:
            return True
        else:
            return False
    else:
        pass
        # raise error


def remove_query2(cursor, table, column, theid):

    match table:
        case 'volunteers':
            query = f'DELETE FROM volunteers WHERE {column} = ?'
            cursor.execute(query, (theid,))
        case 'refugee':
            query = f'DELETE FROM refugee WHERE {column} = ?'
            cursor.execute(query, (theid,))
            if cursor.rowcount > 0:
                return True
            else:
                return False
        case 'camps':
            query = f'DELETE FROM camps WHERE {column} = ?'
            cursor.execute(query, (theid,))
        case 'humanitarianplan':
            query = f'DELETE FROM humanitarianplan WHERE {column} = ?'
            cursor.execute(query, (theid,)) # column is plan_id
        case _:
            pass
            # raise error


def view_table(table):
    with setup_conn() as conn:
        cursor = conn.cursor()
        if table == 'users':
            cursor.execute("SELECT * FROM users")
            for row in cursor.fetchall():
                print(row)
    
        elif table == 'refugee':
            cursor.execute("SELECT * FROM refugee")
            for row in cursor.fetchall():
                return row

        match table:
            case 'camps':
                cursor.execute("SELECT * FROM camps")
                for row in cursor.fetchall():
                    print(row)
            case 'humanitarianplan':
                cursor.execute("SELECT * FROM humanitarianplan")
                for row in cursor.fetchall():
                    print(row)
            case 'ressourcesOld':
                cursor.execute("SELECT * FROM ressourcesOld")
                for row in cursor.fetchall():
                    print(row)

            case 'availability':
                cursor.execute("SELECT * FROM availability")
                for row in cursor.fetchall():
                    print(row)

            case _:
                pass


# AVA
def view_specific_row(planID, table):
    with setup_conn() as conn:
        cursor = conn.cursor()
        match table:
            case 'humanitarianplan':
                cursor.execute("SELECT * FROM humanitarianplan WHERE planID = ?", (planID,))
                for row in cursor.fetchall():
                    print (f"Details for {planID}:{row}")


def update_by_column(cursor, table, column, row_id, where, thedata):
    with setup_conn() as conn:
        cursor = conn.cursor()
        query = f"UPDATE {table} SET {column} = ? WHERE {where} = ?"
        cursor.execute(query, (thedata, row_id))


def update_camp_status_f(cursor, whichcamp, new_status):
    with setup_conn() as conn:
        cursor = conn.cursor()
        query = f"UPDATE camps SET status = ? WHERE campID = ?"
        cursor.execute(query, (new_status, whichcamp))
        # cursor.execute("UPDATE camps SET status = ? WHERE campID = ?", (new_status, whichcamp))

def transfer_camp_r_v(camp_id, new_camp):
    with setup_conn() as conn:
        cursor = conn.cursor()
        query1 = f"UPDATE users SET campID = ? WHERE campID = ?"
        cursor.execute(query1, (new_camp, camp_id))
        query2 = f"UPDATE refugee SET campID = ? WHERE campID = ?"
        cursor.execute(query2, (new_camp, camp_id))

def remaining_resources():
    with setup_conn() as conn:
        cursor = conn.cursor()
        count = cursor.execute('''SELECT c.campID, c.planID,
                                c.capacity AS remainingCapacity,
                                r.glutenFree - c.totalGF AS remainingGF,
                                r.dairyFree - c.totalDF AS remainingDF,
                                r.noNuts - c.totalNN AS remainingNN,
                                r.vegan - c.totalVgn AS remainingVgn,
                                r.vegetarian - c.totalVgt AS remainingVgt,
                                r.omnivore - c.totalOmn AS remainingOmn,
                                r.epipen AS remainingEpipen,
                                r.painRelief AS remainingPainRelief,
                                r.bandages AS remainingBandages,
                                r.sanitaryProducts - c.totalSP AS remainingSP,
                                r.coughsyrup AS remainingCoughsyrup,
                                r.allergyMedication AS remainingAllergy,
                                r.indigestion AS remainingIndigestion,
                                r.skincream AS remainingSkincream
                            FROM
                                camps c
                            JOIN
                                ressourcesOld r ON c.campID = r.campID;
                            '''
        )
        return cursor.fetchall()


def get_count(cursor, table, column, theid): # use to get total volunteers and refugees for camp
    query = f"SELECT COUNT(*) FROM {table} WHERE {column} = ?"
    cursor.execute(query, (theid,))
    count = cursor.fetchone()[0]
    return count


# AVA
def insert_end_date(end_date, input_plan_id):
    with setup_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE humanitarianplan SET end_date =? WHERE planID = ?", (end_date,input_plan_id))


def edit_attribute(input_attribute, new_input, input_plan_id):
    with setup_conn() as conn:
        cursor = conn.cursor()
        query = f"UPDATE humanitarianplan SET {input_attribute} = ? WHERE planID = ?"
        try:
            cursor.execute(query, (new_input, input_plan_id))
            conn.commit()
            if cursor.rowcount>0:
                print(f"Successful edit: {input_attribute} for HP:{input_plan_id} is now {new_input}")
            else:
                print("Successfully executed but no changes have been made")
        except sqlite3.Error as error:
            print(error)



def update_table(cursor, table, thedata):
    if table == 'ressourcesOld':
            camp_id = thedata[0][0] if isinstance(thedata[0], tuple) else thedata[0]
            existing_data = cursor.execute("SELECT * FROM ressourcesOld WHERE campID=?", (camp_id,)).fetchone()

            entry_date = datetime.now().strftime('%Y-%m-%d')           

            if existing_data:
                cursor.execute('''UPDATE ressourcesOld
                               SET 
                                glutenFree = ? + glutenFree,
                                dairyFree = ? + dairyFree,
                                noNuts = ? + noNuts,
                                vegan = ? + vegan,
                                vegetarian = ? + vegetarian,
                                omnivore = ? + omnivore,
                                epipen = ? + epipen,
                                painRelief = ? + painRelief,
                                bandages = ? + bandages,
                                sanitaryProducts = ? + sanitaryProducts,
                                coughsyrup = ? + coughsyrup,
                                allergyMedication = ? + allergyMedication,
                                indigestion = ? + indigestion,
                                skincream = ? + skincream,
                                entryDate = ?
                            WHERE campID = ?
             ''', tuple(thedata[1:]) +(entry_date, camp_id))
            else:
                cursor.execute('''INSERT INTO ressourcesOld (
                               volunteerID, glutenFree, dairyFree, noNuts, vegan,
                               vegetarian, omnivore, epipen, painRelief, bandages,
                               sanitaryProducts, coughsyrup, allergyMedication, 
                               indigestion, skincream, entryDate, campID
                            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',  tuple(thedata[1:]) +(entry_date, camp_id))
    if table == 'ressourcesNew':
        plan_id = thedata[0][0] if isinstance(thedata[0], tuple) else thedata[0]
        existing_data = cursor.execute("SELECT * FROM ressourcesNew WHERE planID = ?", (plan_id,)).fetchone()
        if not existing_data:
            # If there's no existing data, insert new data
            cursor.execute(
                '''INSERT INTO ressourcesNew (
                    newGF, newDairyFree, newNoNuts, newVegan, newVegetarian,
                    newOmnivore, newEpipen, newSanitaryProducts, newPainRelief,
                    newBandages, newCoughsyrup, newAllergyMedication,
                    newIndigestion, newSkincream, planID
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                tuple(thedata[1:]) + (plan_id,)
            )
        

def delete_from_table(cursor, table, thedata):
    if table == 'ressourcesNew':
            camp_id = thedata[0]
            cursor.execute('''SELECT planID FROM camps WHERE campID = ?''', (camp_id,))
            hp_id = cursor.fetchone()

            if hp_id:
                cursor.execute('SELECT * FROM ressourcesNew WHERE planID = ?', (hp_id[0],))
                existing_entry = cursor.fetchone()

                if existing_entry:
                    cursor.execute('''UPDATE ressourcesNew
                                   SET 
                                    newGF = newGF - ?,
                                    newDairyFree = newDairyFree - ?,
                                    newNoNuts = newNoNuts - ? ,
                                    newVegan = newVegan - ?,
                                    newVegetarian = newVegetarian - ?,
                                    newOmnivore = newOmnivore - ?,
                                    newEpipen = newEpipen - ?,
                                    newPainRelief = newPainRelief - ?,
                                    newBandages = newBandages - ?,
                                    newSanitaryProducts = newSanitaryProducts - ?,
                                    newCoughsyrup = newCoughsyrup - ?,
                                    newAllergyMedication = newAllergyMedication - ?,
                                    newIndigestion = newIndigestion - ?,
                                    newSkincream = newSkincream - ?
                                WHERE planID = ?
                ''', tuple(thedata[1:]) +(hp_id[0],))
    

def select_item(column, table, where, data):
    with setup_conn() as conn:
        cursor = conn.cursor()
        match table:
            case 'ressourcesOld':
                cursor.execute(f'SELECT {column} FROM ressourcesOld WHERE {where} = ?', (data,))
                return cursor.fetchone()


def get_id_from_db():
    with setup_conn() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM humanitarianplan ORDER BY planID DESC LIMIT 1;"
        cursor.execute(query)
        row = cursor.fetchone()
        return row[0]



def get_volunteer_id(identifier, which):
    with setup_conn() as conn:
        cursor = conn.cursor()
        match which:
            case '1': #name
                names = identifier.split(" ")
                first_name = names[0] if names else ""
                last_name = names[1] if len(names) > 1 else ""
                query = f"SELECT userID FROM users WHERE name = ? AND surname = ?"
                cursor.execute(query, (first_name, last_name))
                return cursor.fetchone()
            case '2': #username
                query = f"SELECT userID FROM users WHERE username = ?"
                cursor.execute(query, (identifier,))
                return cursor.fetchone()

def get_timeslot_id(day, time):
    with setup_conn() as conn:
        cursor = conn.cursor()
        query = f'SELECT timeSlotID FROM timeSlot WHERE dayOfWeek = ? AND startTime = ?'
        cursor.execute(query, (day, time))
        result = cursor.fetchone()
        if result:
            return result
        else: 
            print("Timeslot not found")

def get_refugee_id(full_name):
    with setup_conn() as conn:
        cursor = conn.cursor()
        names = full_name.split(" ")
        first_name = names[0] if names else ""
        last_name = names[1] if len(names) > 1 else ""
        print(first_name, last_name)
        query = f"SELECT refugeeID FROM refugee WHERE name = ? AND surname = ?"
        cursor.execute(query, (first_name, last_name))
        return cursor.fetchone()
    
def is_available(timeslot_id, user_id):
    with setup_conn() as conn:
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM booking WHERE timeSlotID = ? AND userID = ?"
        cursor.execute(query, (timeslot_id, user_id))
        count = cursor.fetchone()
        return count[0]
    
    
# setup_db()
def update_volunteer(cursor, table, thedata):
        if table == 'ressourcesOld':
            camp_id = thedata[0]
            existing_data = cursor.execute("SELECT * FROM ressourcesOld WHERE campID=?", (camp_id,)).fetchone()

            entry_date = datetime.now().strftime('%Y-%m-%d')           

            if existing_data:
                cursor.execute('''UPDATE ressourcesOld
                               SET 
                                volunteerID = ?,
                                glutenFree = ?,
                                dairyFree = ?,
                                noNuts = ?,
                                vegan = ?,
                                vegetarian = ?,
                                omnivore = ?,
                                epipen = ?,
                                painRelief = ?,
                                bandages = ?,
                                sanitaryProducts = ?,
                                coughsyrup = ?,
                                allergyMedication = ?,
                                indigestion = ?,
                                skincream = ?,
                                entryDate = ?
                            WHERE campID = ?
             ''', tuple(thedata[1:]) +(entry_date, camp_id))
            else:
                cursor.execute('''INSERT INTO ressourcesOld (
                               glutenFree, dairyFree, noNuts, vegan,
                               vegetarian, omnivore, epipen, painRelief, bandages,
                               sanitaryProducts, coughsyrup, allergyMedication, 
                               indigestion, skincream, entryDate, camp_id
                            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',  tuple(thedata[1:]) +(entry_date, camp_id))
