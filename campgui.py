import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from hpava import *
from fcamp import *
import re
import pycountry_convert as pc
from location_api_ava import city_coordinate_converter
from countries import get_country_code
from weather_api_ava import Weather
from resources import new_resources_old


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def update_count(plan_id): # this updates campNo in humanitarianplan table, needs to be called after create and delete camp
    
    count_query = "SELECT COUNT(*) FROM camps WHERE planID = ?"
    cursor.execute(count_query, (plan_id,))
    count_result = cursor.fetchone()[0]

    update_query = "UPDATE humanitarianplan SET campNo = ? WHERE planID = ?"
    cursor.execute(update_query, (count_result, plan_id))
    conn.commit()

def get_hpid(camp_id):
        
        query = "SELECT planID FROM camps WHERE campID = ?"
        cursor.execute(query, (camp_id,))
        result = cursor.fetchone()
        return result[0]

def get_cont(hp_id):
    query = "SELECT location FROM humanitarianplan WHERE planID = ?"
    cursor.execute(query, (hp_id,))
    result = cursor.fetchone()        
    return result[0]
    
def is_country_in_correct_continent(country, expected_continent):

    country = country.capitalize()
    
    europe = ['Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom', 'Vatican City', 'UK', 'England', 'Wales', 'Scotland', 'Northern Ireland']
    asia = ['Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Cambodia', 'China', 'Cyprus', 'Georgia', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar (Burma)', 'Nepal', 'North Korea', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar', 'Russia', 'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka', 'Syria', 'Taiwan', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen']
    africa = ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Congo, Democratic Republic of the', 'Congo, Republic of the', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini (formerly Swaziland)', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe']
    south_america = ['Argentina', 'Belize', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Puerto Rico', 'Uruguay', 'Venezuela']
    north_america = ['United States', 'US', 'United States of America', 'USA', 'Canada', 'America', 'Mexico']
    oceania = ['Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu']

    if expected_continent == 'Europe':
        if country in europe:
            return True
    elif expected_continent == 'Asia':
        if country in asia:
            return True
    elif expected_continent == 'Africa':
        if country in africa:
            return True
    elif expected_continent == 'South America':
        if country in south_america:
            return True
    elif expected_continent == 'North America':
        if country in north_america:
            return True
    elif expected_continent == 'Oceania':
        if country in oceania:
            return True
    else:
        return False

def delete_vs_by_camp_id(camp_id):
    delete_query = "DELETE FROM users WHERE campID = ?"
    cursor.execute(delete_query, (camp_id,))
    cursor.execute("DELETE FROM ressourcesOld WHERE campID = ?", (camp_id,))
    conn.commit()
    return cursor.rowcount

    
def create_camp(parent):
    
    create_menu = tk.Toplevel(parent)
    create_menu.title("Create Camp")
    create_menu.geometry("1500x800")
    
    
    def available_planids():
        
        # Query to fetch plan IDs where end_date is null
        query = "SELECT planID FROM humanitarianplan WHERE end_date IS NULL"
        cursor.execute(query)

        # Fetch all rows from the query
        rows = cursor.fetchall()

        # Extracting plan IDs from rows
        plan_ids = [row[0] for row in rows]
        return plan_ids
    
    plan_ids = available_planids()
    
    # plan ID
    planIdLabel = tk.Label(create_menu, text="Enter plan ID: ")
    planIdLabel.grid(row=1, column=0)
    planIdCombo = ttk.Combobox(create_menu, values=plan_ids, state="readonly")
    planIdCombo.grid(row=1, column=1)
    
    
    # City
    cityLabel = tk.Label(create_menu, text="Camp city: ")
    cityLabel.grid(row=3, column=0)
    cityEntry = tk.Entry(create_menu)
    cityEntry.grid(row=3, column=1)

    # Country
    countryLabel = tk.Label(create_menu, text="Camp country: ") # check if compatible with plan's continent
    countryLabel.grid(row=5, column=0)
    countryEntry = tk.Entry(create_menu)
    countryEntry.grid(row=5, column=1)

    # Capacity
    capacityLabel = tk.Label(create_menu, text="Camp capacity: ")
    capacityLabel.grid(row=7, column=0)
    capacityEntry = tk.Entry(create_menu)
    capacityEntry.grid(row=7, column=1)

    # Status
    statusLabel = tk.Label(create_menu, text="Camp status: ")
    statusLabel.grid(row=9, column=0)
    statusCombo = ttk.Combobox(create_menu, state="readonly")
    statusCombo['values'] = ("Active", "Closed")
    statusCombo.grid(row=9, column=1)

    def is_valid_string(input_string):
        return bool(re.fullmatch(r"[A-Za-z\s]+", input_string))

    def is_valid_country(country):
        return is_valid_string(country)

    def is_valid_city(city):
        return is_valid_string(city)

    def is_valid_capacity(capacity):
        try:
            capacity = int(capacity)
            return 1 <= capacity <= 1000
        except ValueError:
            return False
    
    
    def submit_form():
        
        input_hpid = planIdCombo.get()
        input_city = cityEntry.get()
        input_country = countryEntry.get()
        input_capacity = capacityEntry.get()
        input_status = statusCombo.get()
        input_continent = get_cont(input_hpid)
        
        
        
        
        
        valid = True
        # Validate the inputs
        if not is_valid_country(input_country):
            countryErrorLabel.config(text="Invalid country", fg="red")
            valid = False
        else:
            countryErrorLabel.config(text="")

        if not is_valid_city(input_city):
            cityErrorLabel.config(text="Invalid city", fg="red")
            valid = False
        else:
            cityErrorLabel.config(text="")

        if not is_valid_capacity(input_capacity):
            capacityErrorLabel.config(text="Invalid capacity", fg="red")
            valid = False
        else:
            capacityErrorLabel.config(text="")
            
        if not is_country_in_correct_continent(input_country.capitalize(), input_continent):
            cap_country = input_country.capitalize()
            countryErrorLabel.config(text=f"{cap_country} is not in {input_continent}", fg="red")
            valid = False
        else:
            countryErrorLabel.config(text="")
            
        result = False
        
        if valid:

            location_results = city_coordinate_converter(input_city, get_country_code(input_country), "5cd7288030c7b77ae8ef6fdca18ac418" )

            if location_results == None:
                temperature = 'N/A'
                humidity = 'N/A'
                wind_speed = 'N/A'
                description = 'N/A'
                main_weather = 'N/A'
            else:
                weather_result = Weather.fetch_weather(location_results[0],location_results[1],"9d6ccb7de466e40be62e06d6f4a01d13" )
                temperature, humidity, wind_speed, description, main_weather = weather_result
            
            # add weather suggestions, should be the last camp validation - should be possible to override though
        
            newcamp = Camp(input_hpid, input_country, input_city, input_capacity, 0, 0, input_status, 'Sufficient', 0, 0, 0, 0, 0, 0, 0, temperature, humidity, wind_speed, description, main_weather)
            result = newcamp.create_camp()
            update_count(input_hpid)
            new_resources_old()

        if result is not False:
            tk.messagebox.showinfo("Success", "Camp created") # smh always fail whyyyyyy
        else:
            tk.messagebox.showinfo("Failed", "Failed to create a new camp")

    countryErrorLabel = tk.Label(create_menu, text="", fg="red")
    countryErrorLabel.grid(row=5, column=2)
    cityErrorLabel = tk.Label(create_menu, text="", fg="red")
    cityErrorLabel.grid(row=3, column=2)
    capacityErrorLabel = tk.Label(create_menu, text="", fg="red")
    capacityErrorLabel.grid(row=7, column=2)
    countryErrorLabel2 = tk.Label(create_menu, text="", fg="red")
    countryErrorLabel2.grid(row=5, column=4)

    submitBtn = tk.Button(create_menu, text="Create Camp", command=submit_form)
    submitBtn.grid(row=10, column=0, columnspan=2)
    
    # back to the main menu
    exitBtn = tk.Button(create_menu, text="Exit", command=create_menu.destroy)
    exitBtn.grid(row=11, column=0, columnspan=2)

def view_camps(parent):
    
    # sql
    cursor.execute("SELECT campID, planID, country, city, capacity, totalRefugees, totalVolunteers, status, temperature, humidity, windSpeed, weatherDescription, weather FROM camps")
    camps = cursor.fetchall()
    
    # window title
    camps_window = tk.Toplevel(parent)
    camps_window.title("All camps")
    camps_window.geometry("1500x800")

    columns = ('campID', 'planID', 'country', 'city','capacity', 'totalRefugees', 'totalVolunteers', 'status', 'temperature', 'humidity', 'windSpeed', 'weatherDescription', 'weather')

    tree = ttk.Treeview(camps_window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col.title())
        tree.column(col, width=100)

    for camp in camps:
        tree.insert('', tk.END, values=camp)

    tree.pack(expand=True, fill='both')
    
    # back to the main menu
    back_button = tk.Button(camps_window, text="Back to Main Menu", command=camps_window.destroy)
    back_button.pack()

    tableExp = tk.Label(camps_window, text="This table shows all the camps added to the system.")
    tableExp.pack(side="bottom", pady=10)

def view_camp(parent):
    def show_camp():
        # clear
        for i in tree.get_children():
            tree.delete(i)
        
        camp_id = camp_id_entry.get()
        if not camp_id.isdigit():
            result_label.config(text="Please enter a valid campID.")
            return
        
        # sql
        query = "SELECT campID, planID, country, city, capacity, totalRefugees, totalVolunteers, status, temperature, humidity, windSpeed, weatherDescription, weather FROM camps WHERE campID = ?"
        cursor.execute(query, (camp_id,))
        plan = cursor.fetchone()
        
        # success messages
        if plan:
            tree.insert('', tk.END, values=plan)
            result_label.config(text="")
        else:
            result_label.config(text="No camp found with that ID.")

    # title window
    camp_window = tk.Toplevel(parent)
    camp_window.title("View Camp by ID")
    camp_window.geometry("1500x800")

    instruction_label = tk.Label(camp_window, text="Which campID do you want to see?")
    instruction_label.pack()

    camp_id_entry = tk.Entry(camp_window)
    camp_id_entry.pack()

    submit_button = tk.Button(camp_window, text="Submit", command=show_camp)
    submit_button.pack()

    result_label = tk.Label(camp_window, text="")
    result_label.pack()

    columns = ('campID', 'planID', 'country', 'city','capacity', 'totalRefugees', 'totalVolunteers', 'status', 'temperature', 'humidity', 'windSpeed', 'weatherDescription', 'weather')

    tree = ttk.Treeview(camp_window, columns=columns, show='headings', height=1)
    for col in columns:
        tree.heading(col, text=col.title())
        tree.column(col, width=100)
    tree.pack()
    
    # back to the main menu
    back_button = tk.Button(camp_window, text="Back to Main Menu", command=camp_window.destroy)
    back_button.pack()

def delete_camp(parent):
    
    def d_camp():
        # input and save campID
        camp_id = camp_id_entry.get()
        if not camp_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid campID.")
            return
        
        plan_id = get_hpid(camp_id)
        vs_deleted = delete_vs_by_camp_id(camp_id)
        
        # sql
        cursor.execute("DELETE FROM camps WHERE campID = ?", (camp_id,))
        conn.commit()
        
        # success messages
        if cursor.rowcount == 0:
            messagebox.showinfo("Not found", f"No camp found with ID {camp_id}.")
            
            
        else:
            messagebox.showinfo("Success", f"Camp with ID {camp_id} and its {vs_deleted} associated volunteers have been deleted.")
            cursor.execute("UPDATE refugee SET campID = NULL WHERE campID = ?", (camp_id,))
            update_count(plan_id)
            refresh_treeview()
    
    def refresh_treeview():
        # clear for later refreshing
        for i in tree.get_children():
            tree.delete(i)
            
        cursor.execute("SELECT * FROM camps")
        camps = cursor.fetchall()
        
        for camp in camps:
            tree.insert('', tk.END, values=camp)

    
    
    # title window
    dc_window = tk.Toplevel(parent)
    dc_window.title("Delete Camp by ID")
    dc_window.geometry("1500x800")

    instruction_label = tk.Label(dc_window, text="Enter the campID of the plan you want to delete:")
    instruction_label.pack()

    camp_id_entry = tk.Entry(dc_window)
    camp_id_entry.pack()

    submit_button = tk.Button(dc_window, text="Delete Camp", command=d_camp)
    submit_button.pack()

    columns = ('campID', 'planID', 'country', 'city','capacity', 'totalRefugees', 'totalVolunteers', 'status', 'resoucesState', 'totalGF', 'totalDF', 'totalNN', 'totalVgn', 'totalVgt','totalOmn','totalSP', 'temperature', 'humidity', 'windSpeed', 'weatherDescription', 'weather')

    tree = ttk.Treeview(dc_window, columns=columns, show='headings', height=10)
    for col in columns:
        tree.heading(col, text=col.title())
    refresh_treeview()
    
    tree.pack(expand=True, fill='both')
    
    # back to the main menu
    back_button = tk.Button(dc_window, text="Back to Main Menu", command=dc_window.destroy)
    back_button.pack()
    
def campgui_menu(parent):
    create_camp_button = tk.Button(parent, text="Create new camp", command=lambda: create_camp(parent))
    create_camp_button.pack(pady=10)

    view_camps_button = tk.Button(parent, text="View all camps", command=lambda: view_camps(parent))
    view_camps_button.pack(pady=10)

    view_camp_button = tk.Button(parent, text="View a specific camp", command=lambda: view_camp(parent))
    view_camp_button.pack(pady=10)

    delete_plan_button = tk.Button(parent, text="Delete a camp", command=lambda: delete_camp(parent))
    delete_plan_button.pack(pady=10)
    
    #root.mainloop()


#campgui_menu()
