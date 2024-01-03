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
from weather_suggestions import check_temp
from datetime import datetime
from resources import new_resources_old, new_resources_new


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

def delete_camps_by_plan_id(plan_id):
    delete_query = "DELETE FROM camps WHERE planID = ?"
    cursor.execute(delete_query, (plan_id,))
    cursor.execute("DELETE FROM ressourcesOld WHERE campID IN (SELECT campID FROM camps WHERE planID = ?)", (plan_id,))
    conn.commit()
    return cursor.rowcount


def close_camps_by_plan_id(plan_id):
    update_query = "UPDATE camps SET status = 'Closed' WHERE planID = ?"
    cursor.execute(update_query, (plan_id,))
    conn.commit()
    return cursor.rowcount


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


#gltemperature, glhumidity, glmain_weather, glwind_speed, gldescription = None, None, None, None, None 

def create_hp(parent):

    
    
    create_menu = tk.Toplevel(parent)
    create_menu.title("Create Plan")
    create_menu.geometry("1500x800")

    typeLabel = tk.Label(create_menu, text="HP type: ")
    typeLabel.grid(row=1, column=0)
    typeCombo = ttk.Combobox(create_menu, state="readonly")
    typeCombo['values'] = ("Flood", "Fire", "Volcano", "Tsunami", "War", "Hurricane", "Earthquake", "Nuclear Disaster",
                 "Political Persecution")
    typeCombo.grid(row=1, column=1)
    
    areaLabel = tk.Label(create_menu, text="HP area: ")
    areaLabel.grid(row=3, column=0)
    areaCombo = ttk.Combobox(create_menu, state="readonly")
    areaCombo['values'] = ('Europe', 'South America', 'North America', 'Asia', 'Oceania', 'Africa')
    areaCombo.grid(row=3, column=1)
    
    desLabel = tk.Label(create_menu, text="HP description: ")
    desLabel.grid(row=5, column=0)
    desEntry = tk.Entry(create_menu)
    desEntry.grid(row=5, column=1)
    
    sdLabel = tk.Label(create_menu, text="Enter start date in a yyyy-mm-dd format: ")
    sdLabel.grid(row=7, column=0)
    sdEntry = tk.Entry(create_menu)
    sdEntry.grid(row=7, column=1)
    
    camp_section = tk.Frame(create_menu)
    camp_section.grid(row=12, column=0, columnspan=2)
    camp_section.grid_remove()
    

    # Country
    countryLabel = tk.Label(camp_section, text="Camp country: ") # check if compatible with plan's continent - done
    countryLabel.grid(row=12, column=0)
    countryEntry = tk.Entry(camp_section)
    countryEntry.grid(row=12, column=1)

    # City
    cityLabel = tk.Label(camp_section, text="Camp city: ")
    cityLabel.grid(row=14, column=0)
    cityEntry = tk.Entry(camp_section)
    cityEntry.grid(row=14, column=1)

     #Weather
        
    weatherinfoLabel= tk.Label(camp_section, text="", fg="red")
    weatherinfoLabel.grid(row=20, column=0)
    weathersuggestionLabel= tk.Label(camp_section, text="", fg="red")
    weathersuggestionLabel.grid(row=21, column=0)

    # Capacity
    capacityLabel = tk.Label(camp_section, text="Camp capacity: ")
    capacityLabel.grid(row=16, column=0)
    capacityEntry = tk.Entry(camp_section)
    capacityEntry.grid(row=16, column=1)

    # Status
    statusLabel = tk.Label(camp_section, text="Camp status: ")
    statusLabel.grid(row=18, column=0)
    statusCombo = ttk.Combobox(camp_section, state="readonly")
    statusCombo['values'] = ("Active", "Closed")
    statusCombo.grid(row=18, column=1)
    
    vr_section = tk.Frame(create_menu)
    vr_section.grid(row=20, column=0, columnspan=2)
    vr_section.grid_remove()
    
    vrBtn = tk.Button(vr_section, text="Add volunteers and refugees", command=hpgui_menu) # joseph pls add command
    vrBtn.grid(row=24, column=0, columnspan=2)
    
    def is_valid_string(input_string):
        return bool(re.fullmatch(r"^[A-Za-z\s]+$", input_string))

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
        
    def is_valid_date(d):
        try:
            datetime.strptime(d, '%Y-%m-%d')
            return True  # Valid date format
        except ValueError:
            return False
    


        
   

    def submit_form_camp():

       
        
        last_hp_id = get_id_from_db()
        input_city = cityEntry.get()
        input_country = countryEntry.get()
        input_capacity = capacityEntry.get()
        input_status = statusCombo.get()
        input_continent = get_cont(last_hp_id)


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
            
          
            newcamp = Camp(last_hp_id, input_country, input_city, input_capacity, 0, 0, input_status, 'Sufficient', 0, 0, 0, 0, 0, 0, 0, temperature, humidity, wind_speed, description, main_weather)
            result = newcamp.create_camp()
            new_resources_new()
            new_resources_old()
            update_count(last_hp_id)
       

        if result is not False:
            tk.messagebox.showinfo("Success", "Camp created")
            vr_section.grid()
            exit_section.grid()
        else:
            tk.messagebox.showinfo("Failed", "Failed to create a new camp")

    
    
    submitBtn = tk.Button(camp_section, text="Create Camp", command=submit_form_camp)
    submitBtn.grid(row=22, column=0, columnspan=2)

    def view_weather():

        input_city = cityEntry.get()
        input_country = countryEntry.get()

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

        if not input_city or not input_country:
            weatherinfoLabel.config(text="Enter both country and city to view weather", fg = "red")
            weathersuggestionLabel.config(text="", fg="red")
            valid = False
        

        

        if valid:


            location_results = city_coordinate_converter(input_city, get_country_code(input_country), "5cd7288030c7b77ae8ef6fdca18ac418" )
            if location_results:
                weather_result = Weather.fetch_weather(location_results[0],location_results[1],"9d6ccb7de466e40be62e06d6f4a01d13" )
                temperature, humidity, wind_speed, description, main_weather = weather_result

                if weather_result:
                    weatherinfoLabel.config(text=f"The weather in {input_city} in {input_country} is {main_weather}, more specifically {description}. The current temperature is {temperature} degrees celsius, humidity is {humidity}% and wind speed is {wind_speed}m/s.", fg="red")
                
                    suitable, message = check_temp(temperature)
                    if suitable and message:
                        weathersuggestionLabel.config(text=f"{message}", fg="red")
                    elif suitable and not message:
                        weathersuggestionLabel.config(text="", fg = "red")
                    elif not suitable and message:
                        weathersuggestionLabel.config(text=f"{message}", fg="red")

                    else:
                        weathersuggestionLabel.config(text="", fg="red")

                #tk.messagebox.showinfo("test","weather")
                else:
                    weatherinfoLabel.config(text="Weather not found", fg="red")
                    weathersuggestionLabel.config(text="", fg="red")
                    
            else:
                weatherinfoLabel.config(text="Unable to fetch weather for this location, enter a different city", fg="red")
                weathersuggestionLabel.config(text="", fg="red")


           

       
                #tk.messagebox.showinfo("Please ensure you have entered a correct city and country name")
            #Exception as e:
                #tk.messagebox.showinfo(f"Error {e}")
        
    
    #weather
#f"The weather in {input_city} in {input_country} is {main_weather}, more specifically {description}. The current temperature is {temperature} degrees celsius, humidity is {humidity}% and wind speed is {wind_speed}m/s."
    weatherBtn = tk.Button(camp_section, text="View weather", command=view_weather)
    weatherBtn.grid(row=14, column=3, columnspan=2)
    

    def submit_form():
        input_type = typeCombo.get()
        input_area = areaCombo.get()
        input_des = desEntry.get()
        input_sd = sdEntry.get()
        
        valid = True
        
        if not is_valid_date(input_sd):
            dateErrorLabel.config(text="Invalid date format", fg="red")
            valid = False
        else:
            dateErrorLabel.config(text="")
            
        
        result = False
        
        if valid:
            newplan = HumanitarianPlan(input_type, input_des, input_area, 0, input_sd)
            result = HumanitarianPlan.create_humanitarian_plan(newplan)
            
        if result is not False:
            tk.messagebox.showinfo("Success", "Plan created") 
            camp_section.grid()
            typeCombo.config(state='disabled')
            areaCombo.config(state='disabled')
            desEntry.config(state='disabled')
            sdEntry.config(state='disabled')

        else:
            tk.messagebox.showinfo("Failed", "Failed to create a new plan")

    dateErrorLabel = tk.Label(create_menu, text="", fg="red")
    dateErrorLabel.grid(row=7, column=2)
    
    cityErrorLabel = tk.Label(camp_section, text="", fg="red")
    cityErrorLabel.grid(row=14, column=2)
    
    countryErrorLabel = tk.Label(camp_section, text="", fg="red")
    countryErrorLabel.grid(row=12, column=2)
    
    countryErrorLabel2 = tk.Label(camp_section, text="", fg="red")
    countryErrorLabel2.grid(row=12, column=4)
    
    capacityErrorLabel = tk.Label(camp_section, text="", fg="red")
    capacityErrorLabel.grid(row=16, column=2)
    
    submitBtn = tk.Button(create_menu, text="Create Plan", command=submit_form)
    submitBtn.grid(row=10, column=0, columnspan=2)
    
    # back to the main menu
    exit_section = tk.Frame(create_menu)
    exit_section.grid(row=20, column=0, columnspan=2)
    exit_section.grid_remove()
    
    exitBtn = tk.Button(exit_section, text="Back to Manage Plans Menu", command=create_menu.destroy)
    exitBtn.grid(row=26, column=0, columnspan=2)


def view_hps(parent):
    
    # sql
    cursor.execute("SELECT * FROM humanitarianplan")
    plans = cursor.fetchall()
    
    # window title
    plans_window = tk.Toplevel(parent)
    plans_window.title("Humanitarian Plans")
    plans_window.geometry("1500x800")

    columns = ('planID', 'type', 'description', 'location', 'campNo', 'start_date', 'end_date')

    tree = ttk.Treeview(plans_window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col.title())

    for plan in plans:
        tree.insert('', tk.END, values=plan)

    tree.pack(expand=True, fill='both')
    
    # back to the main menu
    back_button = tk.Button(plans_window, text="Back to Manage Plans Menu", command=plans_window.destroy)
    back_button.pack()

    tableExp = tk.Label(plans_window, text="This table shows all the humanitarian plans added to the system.") 
    tableExp.pack(side="bottom", pady=10)    

def view_hp(parent):
    
    def show_plan():
        # clear
        for i in tree.get_children():
            tree.delete(i)
        
        plan_id = plan_id_entry.get()
        if not plan_id.isdigit():
            result_label.config(text="Please enter a valid planID.")
            return
        
        # sql
        query = "SELECT * FROM humanitarianplan WHERE planID = ?"
        cursor.execute(query, (plan_id,))
        plan = cursor.fetchone()
        
        # success messages
        if plan:
            tree.insert('', tk.END, values=plan)
            result_label.config(text="")
        else:
            result_label.config(text="No plan found with that ID.")

    # title window
    plan_window = tk.Toplevel(parent)
    plan_window.title("View Plan by ID")
    plan_window.geometry("1500x800")

    instruction_label = tk.Label(plan_window, text="Which plan do you want to see?")
    instruction_label.pack()

    plan_id_entry = tk.Entry(plan_window)
    plan_id_entry.pack()

    submit_button = tk.Button(plan_window, text="Submit", command=show_plan)
    submit_button.pack()

    result_label = tk.Label(plan_window, text="")
    result_label.pack()

    columns = ('planID', 'type', 'description', 'location', 'campNo', 'start_date', 'end_date')

    tree = ttk.Treeview(plan_window, columns=columns, show='headings', height=1)
    for col in columns:
        tree.heading(col, text=col.title())
    tree.pack()
    
    # back to the main menu
    back_button = tk.Button(plan_window, text="Back to Manage Plans Menu", command=plan_window.destroy)
    back_button.pack()

def edit_hp(parent):
    
    def fetch_plan():
        # clear
        for i in tree.get_children():
            tree.delete(i)
        for widget in edit_area.winfo_children():
            widget.destroy()

        # input and save planID
        plan_id = plan_id_entry.get()
        if not plan_id.isdigit():
            result_label.config(text="Please enter a valid planID.")
            return
        
        # sql
        query = "SELECT * FROM humanitarianplan WHERE planID = ?"
        cursor.execute(query, (plan_id,))
        plan = cursor.fetchone()
        
        if plan:
            tree.insert('', tk.END, values=plan)
            result_label.config(text="")
            create_edit_interface()
        else:
            result_label.config(text="No plan found with that ID.")

    def create_edit_interface(): #what for
        category_label = tk.Label(edit_area, text="Which category do you want to edit?")
        category_label.pack()
        
        categories = ('type', 'description', 'location', 'start_date')
        category_combo = ttk.Combobox(edit_area, values=categories, state="readonly")
        category_combo.pack()
        
        def category_selected(event=None):
            for widget in input_area.winfo_children(): # maybe delete
                widget.destroy()
             
            category = category_combo.get()
            new_value_label = tk.Label(input_area, text=f"Enter new {category}:")
            new_value_label.pack()
            
            if category in ['type', 'location']:
                options = {'type': ["Flood", "Fire", "Volcano", "Tsunami", "War", "Hurricane", "Earthquake", "Nuclear Disaster",
                 "Political Persecution"],
                           'location': ["Europe", "Asia", "Africa", "South America", "North America", "Australia"]}
                new_value_combo = ttk.Combobox(input_area, values=options[category], state="readonly")
                new_value_combo.pack()
                save_button = tk.Button(input_area, text="Save", command=lambda: update_plan(category, new_value_combo.get()))
                save_button.pack()
            elif category in ['description', 'start_date']:
                new_value_entry = tk.Entry(input_area)
                new_value_entry.pack()
                save_button = tk.Button(input_area, text="Save", command=lambda: update_plan(category, new_value_entry.get()))
                save_button.pack()
        
        category_combo.bind('<<ComboboxSelected>>', lambda event: category_selected())

    def is_valid_date(d):
        try:
            datetime.strptime(d, '%Y-%m-%d')
            return True  # Valid date format
        except ValueError:
            return False
        
    def update_plan(category, new_value):
        
        error_message = ""
        valid = True
        
        if category.lower() == 'start_date' and not is_valid_date(new_value):
            valid = False
            error_message = "Invalid date. Please enter a valid date in yyyy-mm-dd format."
        
        if valid:
        
            plan_id = plan_id_entry.get()
            query = f"UPDATE humanitarianplan SET {category} = ? WHERE planID = ?"
            cursor.execute(query, (new_value, plan_id))
            conn.commit()
            result_label.config(text=f"Plan {plan_id} updated: {category} set to {new_value}.")
            fetch_plan()  # refreshhhh
        
        else: 
            result_label.config(text=error_message, foreground="red")

    # title window
    edit_window = tk.Toplevel(parent)
    edit_window.title("Edit Plan")
    edit_window.geometry("1500x800")

    tk.Label(edit_window, text="Enter the planID of the plan you want to edit:").pack()
    plan_id_entry = tk.Entry(edit_window)
    plan_id_entry.pack()

    submit_button = tk.Button(edit_window, text="Fetch Plan", command=fetch_plan)
    submit_button.pack()

    result_label = tk.Label(edit_window, text="")
    result_label.pack()

    columns = ('planID', 'type', 'description', 'location', 'campNo', 'start_date', 'end_date')
    tree = ttk.Treeview(edit_window, columns=columns, show='headings', height=1)
    for col in columns:
        tree.heading(col, text=col.title())
    tree.pack()

    edit_area = tk.LabelFrame(edit_window, text="Edit Area")
    edit_area.pack(fill="x", expand="yes")

    input_area = tk.LabelFrame(edit_window, text="Input Area")
    input_area.pack(fill="x", expand="yes")
    
    # back to the main menu
    back_button = tk.Button(edit_window, text="Back to Manage Plans Menu", command=edit_window.destroy)
    back_button.pack()

def delete_hp(parent):
    
    def delete_plan():
        # input and save planID
        plan_id = plan_id_entry.get()
        if not plan_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid planID.")
            return
        
        cursor.execute("SELECT campID FROM camps WHERE planID = ?", (plan_id,))
        camp_ids2 = [row[0] for row in cursor.fetchall()]
        for camp_id1 in camp_ids2:
            cursor.execute("DELETE FROM users WHERE campID = ?", (camp_id1,))
            cursor.execute("DELETE FROM refugee WHERE campID = ?", (camp_id1,))

   
   
        camps_deleted = delete_camps_by_plan_id(plan_id)
        
        # sql
        cursor.execute("DELETE FROM humanitarianplan WHERE planID = ?", (plan_id,))
        cursor.execute("DELETE FROM ressourcesNew WHERE planID = ?", (plan_id,))
        conn.commit()
        
        # success messages
        if cursor.rowcount == 0:
            messagebox.showinfo("Not found", f"No plan found with ID {plan_id}.")
        else:
            messagebox.showinfo("Success", f"Plan with ID {plan_id} and its {camps_deleted} associated camps have been deleted.")
            refresh_treeview()
    
    def refresh_treeview():
        # clear for later refreshing
        for i in tree.get_children():
            tree.delete(i)
            
        cursor.execute("SELECT * FROM humanitarianplan")
        plans = cursor.fetchall()
        
        for plan in plans:
            tree.insert('', tk.END, values=plan)

    
    # title window
    dp_window = tk.Toplevel(parent)
    dp_window.title("Delete Plan by ID")
    dp_window.geometry("1500x800")

    instruction_label = tk.Label(dp_window, text="Enter the planID of the plan you want to delete:")
    instruction_label.pack()

    plan_id_entry = tk.Entry(dp_window)
    plan_id_entry.pack()

    submit_button = tk.Button(dp_window, text="Delete Plan", command=delete_plan)
    submit_button.pack()
    

    columns = ('planID', 'type', 'description', 'location', 'campNo', 'start_date', 'end_date')

    tree = ttk.Treeview(dp_window, columns=columns, show='headings', height=10)
    for col in columns:
        tree.heading(col, text=col.title())
    refresh_treeview()
    
    tree.pack(expand=True, fill='both')
    
    # back to the main menu
    back_button = tk.Button(dp_window, text="Back to Manage Plans Menu", command=dp_window.destroy)
    back_button.pack()

def close_hp(parent):
    
    def close_plan():
        # input save planID
        plan_id = plan_id_entry.get()
        end_date = ed_entry.get()

        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            if end_date < datetime.now():
                messagebox.showerror("Error","End date cannot be before today")
                return
        except ValueError:
            messagebox.showerror("Error","Date format incorrect, you must enter date in the format YYYY-MM-DD")
            return

       
        if not plan_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid planID.")
            return
        
        cursor.execute("SELECT campID FROM camps WHERE planID = ?", (plan_id,))
        camp_ids2 = [row[0] for row in cursor.fetchall()]
        for camp_id1 in camp_ids2:
            cursor.execute("UPDATE users SET status = 'inactive' WHERE campID = ?", (camp_id1,))
            
            
        camps_closed = close_camps_by_plan_id(plan_id)
        
        # sql
        cursor.execute("UPDATE humanitarianplan SET end_date =? WHERE planID = ?", (end_date, plan_id))
        conn.commit()
        
        # success message
        if cursor.rowcount == 0:
            messagebox.showinfo("Not found", f"No plan found with ID {plan_id}.")
        else:
            messagebox.showinfo("Success", f"Plan with ID {plan_id} and its {camps_closed} associated camps have been closed.")
            refresh_treeview()
    
    def refresh_treeview():

        for i in tree.get_children():
            tree.delete(i)

        cursor.execute("SELECT * FROM humanitarianplan")
        plans = cursor.fetchall()

        for plan in plans:
            tree.insert('', tk.END, values=plan)

    
    # title window
    cp_window = tk.Toplevel(parent)
    cp_window.title("Close Plan by ID")
    cp_window.geometry("1500x800")

    instruction_label = tk.Label(cp_window, text="Enter the planID of the plan you want to close:")
    instruction_label.pack()

    plan_id_entry = tk.Entry(cp_window)
    plan_id_entry.pack()
    
    instruction_label2 = tk.Label(cp_window, text="Enter the end date (YYYY-MM-DD):")
    instruction_label2.pack()

    ed_entry = tk.Entry(cp_window)
    ed_entry.pack()

    submit_button = tk.Button(cp_window, text="Close Plan", command=close_plan)
    submit_button.pack()

    columns = ('planID', 'type', 'description', 'location', 'campNo', 'start_date', 'end_date')

    tree = ttk.Treeview(cp_window, columns=columns, show='headings', height=10)
    for col in columns:
        tree.heading(col, text=col.title())

    refresh_treeview()
    
    tree.pack(expand=True, fill='both')
    
    # back to the main menu
    back_button = tk.Button(cp_window, text="Back to Manage Plans Menu", command=cp_window.destroy)
    back_button.pack()

def hpgui_menu(parent):
    create_plan_button = tk.Button(parent, text="Create new plan", command=lambda: create_hp(parent))
    create_plan_button.pack(pady=10)

    view_plans_button = tk.Button(parent, text="View all plans", command=lambda: view_hps(parent))
    view_plans_button.pack(pady=10)

    view_plan_button = tk.Button(parent, text="View a specific plan", command=lambda: view_hp(parent))
    view_plan_button.pack(pady=10)

    edit_plan_button = tk.Button(parent, text="Edit humanitarian plan", command=lambda: edit_hp(parent))
    edit_plan_button.pack(pady=10)

    delete_plan_button = tk.Button(parent, text="Delete humanitarian plan", command=lambda: delete_hp(parent))
    delete_plan_button.pack(pady=10)

    close_plan_button = tk.Button(parent, text="Close humanitarian plan", command=lambda: close_hp(parent))
    close_plan_button.pack(pady=10)
    
    #parent.mainloop()


#hpgui_menu()
