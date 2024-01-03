import install_libraries
install_libraries.install_all()
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
import refugee_gui
from connectdb import *
from populatedb import pop_db
from refugee_gui import *
from populatedb import pop_db
from hpgui import hpgui_menu
from campgui import campgui_menu
from vgui import volunteer_menu
import pycountry_convert as pc
from schedulling_system_gui import *

setup_db()
pop_db()

class volunteerWindow:
    def __init__(self, master, username, password, session, login_window):
        self.master = master
        self.username = username
        self.password = password
        self.session = session
        self.login_window = login_window
        self.master.geometry("1500x800")
        self.master.title("Volunteer menu")
        logout_button = Button(self.master, text="Logout", command=self.logout)
        logout_button.pack(side=RIGHT, anchor='ne', padx=10, pady=10)
        # Create tabControl to be it easier to use the GUI
        self.tabControl = ttk.Notebook(self.master)
        # Make five tabs: Volunteer info, manage refugees, camps and ressources
        self.volunteer_info = Frame(self.tabControl)
        self.volunteer_schedule = Frame(self.tabControl)
        self.manage_refugee = Frame(self.tabControl)
        self.manage_camp = Frame(self.tabControl)
        self.view_resources = Frame(self.tabControl)
        # self.view_camp = Frame(self.tabControl) 
        self.tabControl.add(self.volunteer_info, text="Volunteer information")
        self.tabControl.add(self.volunteer_schedule, text="Schedule")
        self.tabControl.add(self.manage_refugee, text="Manage Refugee")
        self.tabControl.add(self.view_resources, text="View Resources")
        # self.tabControl.add(self.view_camp, text="View Camp")
        self.tabControl.pack(expand=1, fill='both')

        self.view_camp = Frame(self.tabControl)
        self.tabControl.add(self.view_camp, text="View Camp")
        self.tabControl.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        # Tab information
        for key in self.session:
            text_print = f"{key}: {self.session[key]}"
            information = Label(self.volunteer_info, text=text_print)
            information.pack()


        # Tab resources
        columns = ["Camp ID", "Volunteer ID", "Entry Date", "Gluten Free", "Dairy Free", "No nuts", "Vegan",
                   "Vegetarian", "Omnivore", "Epipen", "Sanitary Products", "Pain Relief", "Bandages", "Cough Syrup", "Allergy medication", "Indigestion", "Skincream"]
        self.table_r = ttk.Treeview(self.view_resources, columns=columns, show='headings')
        with setup_conn() as conn:
            cursor = conn.cursor()
            camp_id = self.session['camp_id']
            cursor.execute("SELECT * FROM ressourcesOld WHERE campID = ?", (camp_id,))
            resources_rows = cursor.fetchall()

            for col in columns:
                self.table_r.heading(col, text=col)
                self.table_r.column(col, width=100, anchor=CENTER)

            for row in resources_rows:

                self.table_r.insert("", END, values=row)

            self.table_r.pack()

            self.edit_resources_v_b = Button(self.view_resources, text="Edit resources", command=self.edit_r_v)
            self.edit_resources_v_b.pack()

            tableExp = tk.Label(self.view_resources, text="This table shows the resources in your camp inventory.") 
            tableExp.pack(side="bottom", pady=10)

        self.refugee_menu()
        self.setup_schedule_tab()

    def on_tab_selected(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View Camp":
            columns = ['campID', 'planID', 'country', 'city','capacity', 'totalRefugees', 'totalVolunteers', 'status', 'temperature', 'humidity', 'windSpeed', 'weatherDescription', 'weather']
            self.table_c = ttk.Treeview(self.view_camp, columns=columns, show='headings')
            with setup_conn() as conn:
                cursor = conn.cursor()
                camp_id = self.session['camp_id']
                cursor.execute("SELECT campID, planID, country, city, capacity, totalRefugees, totalVolunteers, status, temperature, humidity, windSpeed, weatherDescription, weather FROM camps WHERE campID = ?", (camp_id,))
                camp_rows = cursor.fetchall()

                for col in columns:
                    self.table_c.heading(col, text=col)
                    self.table_c.column(col, width=100, anchor=CENTER)

                for row in camp_rows:

                    self.table_c.insert("", END, values=row)

                self.table_c.pack()

                tableExp = tk.Label(self.view_camp, text="This table shows the details of your camp.") 
                tableExp.pack(side="bottom", pady=10)               


    def setup_schedule_tab(self):
        label = Label(self.volunteer_schedule, text="Volunteer Schedule")
        label.grid(row=0, column=0)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            label = Label(self.volunteer_schedule, text=day)
            label.grid(row=5, column=i)

        start_date = datetime.now().replace(day=1)
        for i in range(31):
            current_date = start_date + timedelta(days=i)
            day = current_date.day
            btn = Button(self.volunteer_schedule, text=str(day), command=lambda date=current_date: self.toggle_booking(date))
            row, col = divmod(i + start_date.weekday(), 7)
            btn.grid(row=row + 1, column=col)

        view_schedule = Button(self.volunteer_schedule, text="View schedule", command=self.display_booked_dates)
        view_schedule.grid()

    def display_booked_dates(self):
        view_booked_dates = tk.Tk()
        view_booked_dates.title("Your bookings")
        view_booked_dates.geometry("600x300")

        booking_dates = self.fetch_user_booking_data(self.session['userID'])
        booked_dates_label = Label(view_booked_dates, text="Booked Dates:\n" + "\n".join(booking_dates))
        booked_dates_label.pack()

    def fetch_user_booking_data(self, user_id):
        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT bookingDate FROM bookings WHERE userID = ?", (user_id,))
            booking_dates = [row[0] for row in cursor.fetchall()]

        return booking_dates

    def toggle_booking(self, date):
        user_id = self.session['userID']
        username = self.session['username']

        try:
            if self.can_user_book(user_id, date):
                with setup_conn() as conn:
                    cursor = conn.cursor()
                    check_query = "SELECT bookingID FROM bookings WHERE userID = ? AND bookingDate = ?"
                    check_values = (user_id, date.strftime('%Y-%m-%d'))
                    cursor.execute(check_query, check_values)
                    existing_booking = cursor.fetchone()

                if existing_booking:
                    with setup_conn() as conn:
                        cursor = conn.cursor()
                        delete_query = "DELETE FROM bookings WHERE bookingID = ?"
                        delete_values = (existing_booking[0],)
                        cursor.execute(delete_query, delete_values)

                    tk.messagebox.showinfo("Success", message=f"Booking removed for user {username} on {date.strftime('%Y-%m-%d')}")
                    # removed_booking.grid(row=15, column=25)

                else:
                    with setup_conn() as conn:
                        cursor = conn.cursor()
                        insert_query = "INSERT INTO bookings (userID, bookingDate) VALUES (?, ?)"
                        insert_values = (user_id, date.strftime('%Y-%m-%d'))
                        cursor.execute(insert_query, insert_values)

                    tk.messagebox.showinfo("Success", message=f"Booking added for user {username} on {date.strftime('%Y-%m-%d')}")
                    # succcessful_booking.grid(row=15, column=25)
            else:
                tk.messagebox.showinfo("Success", message="Booking not allowed due to availability restrictions.")
                # unsucccessful_booking.grid(row=15, column=25)

        except sqlite3.Error as e:
            print("Error:", e)

    def get_user_id(self, username):
        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT userID FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()[0]
        return user_id


    def can_user_book(self, user_id, date):
        availability = self.get_user_bookings(user_id)
        if availability == "full-time":
            return True
        elif availability == "part-time":
            booking_count = self.count_weekly_bookings(user_id, date)
            return booking_count < 3
        else:
            return False


    def get_user_bookings(self, user_id):
        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT availability FROM users WHERE userID = ?", (user_id,))
            availability = cursor.fetchone()[0]

        return availability

    def count_weekly_bookings(self, user_id, date):
        start_of_week = date - timedelta(days=date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        query = """
        SELECT COUNT(*) FROM bookings
        WHERE userID = ?
        AND bookingDate BETWEEN ? AND ?
        """
        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id, start_of_week, end_of_week))
            count = cursor.fetchone()[0]

        return count

    def refugee_menu(self):
        create_refugee_button = tk.Button(self.manage_refugee, text="Create Refugee", command=create_refugee)
        create_refugee_button.pack(pady=10)

        delete_refugee_button = tk.Button(self.manage_refugee, text="Delete Refugee", command=delete_refugee)
        delete_refugee_button.pack(pady=10)

        view_refugee_button = tk.Button(self.manage_refugee, text="View Refugee", command=view_refugee)
        view_refugee_button.pack(pady=10)

        search_refugee_button = tk.Button(self.manage_refugee, text="Search Refugee", command=search_refugee)
        search_refugee_button.pack(pady=10)

        edit_refugee_button = tk.Button(self.manage_refugee, text="Edit Refugee", command=edit_refugee)
        edit_refugee_button.pack(pady=10)

        view_family_button = tk.Button(self.manage_refugee, text="View All Family", command=view_by_family)
        view_family_button.pack(pady=10)

        search_family_button = tk.Button(self.manage_refugee, text="Search Family", command=search_family_menu)
        search_family_button.pack(pady=10)

        medic_attention_button = tk.Button(self.manage_refugee, text="Medic Attention", command=medic_attention)
        medic_attention_button.pack(pady=10)

    def edit_r_v(self):
        self.inventory_v = Toplevel(self.view_resources)
        self.inventory_v.title("Allocating resources")
        self.inventory_v.geometry("1500x800")

        food_categories1 = ["GF",  "Dairy Free", "No nuts", "Vegan"]
        food_categories2 = ["Vegetarian", "Omnivore"]
        medicine_categories1 = ["Epipen", "Sanitary Products", "Pain Relief", "Bandages"]
        medicine_categories2 = ["Cough Syrup", "Allergy medication", "Indigestion", "Skincream"]
        categories = ["GF",  "Dairy Free", "No nuts", "Vegan", "Vegetarian", "Other", "Epipen", "Sanitary Products", "Pain Relief", "Bandages", "Cough Syrup", "Allergy medication", "Indigestion", "Skincream"]
        self.category_entry = {}
        food_label = Label(self.inventory_v, text="Food Packets", font=("Helvetica", 12, "bold"))
        food_label.pack(fill='x')

        food_frame1 = Frame(self.inventory_v)
        food_frame1.pack(fill='x')
        
        for i, category in enumerate(food_categories1):
            label_cat = Label(food_frame1, text=f"{category}: ",  width=15)
            label_cat.pack(side='left')

            entry_var = StringVar()
            entry = Entry(food_frame1, textvariable=entry_var, width=10)
            entry.pack(side='left', padx=5)

            self.category_entry[category] = entry
            

        food_frame2 = Frame(self.inventory_v)
        food_frame2.pack(fill='x')
        
        for i, category in enumerate(food_categories2):
            label_cat = Label(food_frame2, text=f"{category}: ",  width=15)
            label_cat.pack(side='left')

            entry_var = StringVar()
            entry = Entry(food_frame2, textvariable=entry_var, width=10)
            entry.pack(side='left', padx=5)

            self.category_entry[category] = entry
            
        medicine_label = Label(self.inventory_v, text="Medicine", font=("Helvetica", 12, "bold"))
        medicine_label.pack(fill='x')

        medicine_frame1 = Frame(self.inventory_v)
        medicine_frame1.pack(fill='x')

        for i, category in enumerate(medicine_categories1):
            label_cat = Label(medicine_frame1, text=f"{category}: ", width=15)
            label_cat.pack(side='left')

            entry_var = StringVar()
            entry = Entry(medicine_frame1, textvariable=entry_var, width=10)
            entry.pack(side='left', padx=5)

            self.category_entry[category] = entry
        
        medicine_frame2 = Frame(self.inventory_v)
        medicine_frame2.pack(fill='x')
        
        for i, category in enumerate(medicine_categories2):
            label_cat = Label(medicine_frame2, text=f"{category}: ", width=15)
            label_cat.pack(side='left')

            entry_var = StringVar()
            entry = Entry(medicine_frame2, textvariable=entry_var, width=10)
            entry.pack(side='left', padx=5)

            self.category_entry[category] = entry

        update_v_button = Button(self.inventory_v, text="Update resources", command=self.update_inventory)
        update_v_button.pack()
        exitBtn_r = Button(self.inventory_v, text="Exit", command=self.inventory_v.destroy)
        exitBtn_r.pack()
    
    def update_inventory(self):
        camp_id = self.session['camp_id']
        volunteer_id = self.session['userID']
        valid = True
        for entry in self.category_entry.values():
            try:
                value = int(entry.get())
                if value < 0:
                    valid = False
                    Label(self.inventory_v, text="Error: Input must be a positive integer").pack()
            except ValueError:
                Label(self.inventory_v, text="Error: Input must be a positive integer").pack()

        if valid:
            category_values = {category: entry.get() for category, entry in self.category_entry.items()}
            category_values = {category: int(value) for category, value in category_values.items()}
            data = (camp_id,)+ (volunteer_id,) + tuple(category_values.values())

            with setup_conn() as conn:
                cursor = conn.cursor()
                update_volunteer(cursor, 'ressourcesOld', data)
                conn.commit()
                self.inventory_v.destroy()
                self.refresh_v()

    

    def refresh_v(self):
        self.table_r.delete(*self.table_r.get_children())
        self.table_r.destroy()
        
        self.edit_resources_v_b.destroy()
        columns = ["Camp ID", "Volunteer ID", "Entry Date", "Gluten Free", "Dairy Free", "No nuts", "Vegan",
                    "Vegetarian", "Omnivore", "Epipen", "Sanitary Products", "Pain Relief", "Bandages", "Cough Syrup", "Allergy medication", "Indigestion", "Skincream"]
        self.table_r = ttk.Treeview(self.view_resources, columns=columns, show='headings')
        with setup_conn() as conn:
            cursor = conn.cursor()
            conn.commit()
            camp_id = self.session['camp_id']
            cursor.execute("SELECT * FROM ressourcesOld WHERE campID = ?", (camp_id,))
            resources_rows = cursor.fetchall()
            print(resources_rows)

            for col in columns:
                self.table_r.heading(col, text=col)
                self.table_r.column(col, width=100, anchor=CENTER)

            for row in resources_rows:

                self.table_r.insert("", END, values=row)

            self.table_r.pack()

            self.edit_resources_v_b = Button(self.view_resources, text="Edit resources", command=self.edit_r_v)
            self.edit_resources_v_b.pack()



        # # Tab manage refugee
        # refugee_menu(self.manage_refugee)

    def edit_volunteer(self):
        self.session.pack_forget()
        self.button_edit.pack_forget()

        self.userId_label = Label(self.volunteer_info, text="UserID: ").pack()
        user_id_value = self.session.cget("userID")

        self.user_id_var = StringVar(value=user_id_value)
        Entry(self.volunteer_info, textvariable=self.user_id_var, state='readonly').pack()

    def logout(self):
        self.master.destroy()
        refugee_gui.logout()
        self.login_window.master.destroy()
        window = Tk()
        frame = Frame(window, relief='sunken')
        window.geometry("+100+100")
        loginWindow(window, frame, handle_result)


class adminWindow:
    def __init__(self, master, login_window):
        self.master = master
        self.login_window = login_window
        self.master.geometry("1500x800")
        self.master.title("Admin menu")
        self.session = {
            'name': 'The',
            'surname': 'Admin',
            'phone': '+44 0000 00000',
            'status': 'active'
        }
        logout_button = Button(self.master, text="Logout", command=self.logout)
        logout_button.pack(side=RIGHT, anchor='ne', padx=10, pady=10)
        self.tabControl = ttk.Notebook(self.master)
        self.manage_volunteer = Frame(self.tabControl)
        # Make five tabs: Volunteer info, manage refugees, camps and ressources
        
        self.admin_info = Frame(self.tabControl)
        self.tabControl.add(self.admin_info, text="Admin information")
        
        # self.manage_plans = Frame(self.tabControl)
        self.manage_resources = Frame(self.tabControl)
        self.tabControl.add(self.manage_resources, text="Manage resources")
        self.tabControl.bind("<<NotebookTabChanged>>", self.refresh_tables)
        self.tabControl.pack(expand=1, fill='both')
        
        

        
        self.manage_plans = Frame(self.tabControl)
        self.tabControl.add(self.manage_plans, text="Manage Plans")
                
        self.manage_camps = Frame(self.tabControl)
        self.tabControl.add(self.manage_camps, text="Manage Camps")
        
        self.manage_volunteers = Frame(self.tabControl)
        self.tabControl.add(self.manage_volunteers, text="Manage Volunteers")
        
        self.tabControl.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        #Tab information
        
        

        #volunteer management


        #ressources: view
        #find which camps have low resources:


    
    def clear_frame(self, frame):
        # Function to clear all widgets from a frame
        for widget in frame.winfo_children():
            widget.destroy()
            
    def on_tab_selected(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "Manage Plans":
            self.clear_frame(self.manage_plans)
            hpgui_menu(self.manage_plans)
            
        elif tab_text == "Manage Camps":
            self.clear_frame(self.manage_camps)
            campgui_menu(self.manage_camps) 
        
        elif tab_text == "Manage Volunteers":
            self.clear_frame(self.manage_volunteers)
            volunteer_menu(self.manage_volunteers)
        elif tab_text == 'Admin information':
            self.clear_frame(self.admin_info)
            greeting_label = Label(self.admin_info, text="Hello Admin!", fg='green', font=("Helvetica", 24))
            greeting_label.pack(pady=(10, 0))
            
            open_hps = 0
            open_camps = 0
            
            with setup_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM humanitarianplan WHERE end_date IS NULL")
                open_hps = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM camps WHERE status = 'Active'")
                open_camps = cursor.fetchone()[0]
            

            info1_label = Label(self.admin_info, text=f"There are currently {open_hps} open humanitarian plans and {open_camps} active camps.", fg='green', font=("Helvetica", 16))
            info1_label.pack(pady=(10, 0))
            
            info2_label = Label(self.admin_info, text="Personal information:", fg='green', font=("Helvetica", 14))
            info2_label.pack(pady=(10, 0))
            for key in self.session:
                text_print = f"{key}: {self.session[key]}"
                information = Label(self.admin_info, text=text_print)
                information.pack(pady=(2, 0))
        elif tab_text == 'Manage resources':
            self.clear_frame(self.manage_resources)
            new_label = Label(self.manage_resources, text="New available resources")
            new_label.pack()
            new_columns = ["Humanitarian Plan", "GF",  "Dairy Free", "No nuts", "Vegan", "Vegetarian", "Other", "Epipen", "Sanitary Products", "Pain Relief", "Bandages", "Cough Syrup", "Allergy medication", "Indigestion", "Skincream"]
            self.table_new = ttk.Treeview(self.manage_resources, columns=new_columns, show='headings')
            with setup_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ressourcesNew")
                new_rows = cursor.fetchall()
            for col in new_columns:
                self.table_new.heading(col, text=col)
                self.table_new.column(col, width=100, anchor=CENTER)
            for row in new_rows:
                self.table_new.insert("", END, values=row)
            self.table_new.pack()
            with setup_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT campID FROM camps")
                self.camp_ids = cursor.fetchall()
                self.camp_id_var = StringVar()
                self.camp_id_multiple = ttk.Combobox(self.manage_resources, textvariable=self.camp_id_var, values=self.camp_ids, state='readonly')
                self.camp_id_multiple.set("Select the camp ID")
                self.camp_id_l = Label(self.manage_resources, text="Camp ID: ")
                self.camp_id_l.pack()
                self.camp_id_multiple.pack()


            
            #displaying the remaining items
            
            self.remaining_label = Label(self.manage_resources, text="Remaining resources")
            self.remaining_label.pack()
            remaining_columns = ["Camp", "Humanitarian Plan", "Remaining Capacity", "Remaining GF", "Remaining Dairy Free", "Remaining No Nuts", "Remaining Vegan", "Remaining vegetarian", "Remaining Other", "Remaining Epipen", "Remaining sanitary products", "Remaining Pain Relief", " Remaining Bandages", "Remaining Cough Syrup", "Remaining Allergy medication", "Remaining Indigestion", "Remaining Skincream"]
            self.table_remaining = ttk.Treeview(self.manage_resources, columns= remaining_columns, show='headings')
            remaining_rows = remaining_resources()
            for col in remaining_columns:
                self.table_remaining.heading(col, text=col)
                self.table_remaining.column(col, width=100, anchor=CENTER)
            for row in remaining_rows:
                self.table_remaining.insert("", END, values=row)
            self.table_remaining.pack()

            self.manage_r_button = Button(self.manage_resources, text="Allocate ressources", command= self.allocate_ressources)
            self.manage_r_button.pack()

    def logout(self):
        self.master.destroy()
        self.login_window.master.destroy()
            
    def get_hpid(self, camp_id):
            
        query = "SELECT planID FROM camps WHERE campID = ?"
        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (camp_id,))
            result = cursor.fetchone()
        return result[0]

    def r_res_two(self, camp_id):
        with setup_conn() as conn:
            cursor = conn.cursor()
            count = cursor.execute('''SELECT r.glutenFree - c.totalGF AS remainingGF,
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
                                    ressourcesOld r ON c.campID = r.campID
                                WHERE c.campID = ?;''', (camp_id,)) 
                                
            return cursor.fetchall()

    def allocate_ressources(self):
        self.allocate_window = Toplevel(self.manage_resources)
        self.allocate_window.title("Allocating resources")
        self.allocate_window.geometry("1500x800")
        food_categories1 = ["GF",  "Dairy Free", "No nuts", "Vegan"]
        food_categories2 = ["Vegetarian", "Omnivore"]
        medicine_categories1 = ["Epipen", "Sanitary Products", "Pain Relief", "Bandages"]
        medicine_categories2 = ["Cough Syrup", "Allergy medication", "Indigestion", "Skincream"]


        selected_camp_id = self.camp_id_var.get()
        selected_camp_id = int(selected_camp_id)
        selected_hp_id = self.get_hpid(selected_camp_id)
        
        new_label1 = Label(self.allocate_window, text=f"Resources available for camp {selected_camp_id} under plan {selected_hp_id}.", font=("Helvetica", 12, "bold"))
        new_label1.pack(fill='x')
        
        new_columns1 = [ "GF",  "Dairy Free", "No nuts", "Vegan", "Vegetarian", "Omnivore", "Epipen", "Sanitary Products", "Pain Relief", "Bandages", "Cough Syrup", "Allergy medication", "Indigestion", "Skincream"]
        self.table_new1 = ttk.Treeview(self.allocate_window, columns=new_columns1, show='headings', height=1)

        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT newGF, newDairyFree, newNoNuts, newVegan, newVegetarian, newOmnivore, newEpipen, newSanitaryProducts, newPainRelief, newBandages, newCoughsyrup, newAllergyMedication, newIndigestion, newSkincream FROM ressourcesNew where planID = ?", (selected_hp_id,))
            new_rows1 = cursor.fetchall()
        for col in new_columns1:
            self.table_new1.heading(col, text=col)
            self.table_new1.column(col, width=100, anchor=CENTER)
        for row in new_rows1:
            self.table_new1.insert("", END, values=row)
            
        self.table_new1.pack(fill='x', padx=10, pady=10) 
        
        new_label2 = Label(self.allocate_window, text=f"Resources remaining in camp {selected_camp_id}.", font=("Helvetica", 12, "bold"))
        new_label2.pack(fill='x')
        
        new_columns2 = [ "GF",  "Dairy Free", "No nuts", "Vegan", "Vegetarian", "Omnivore", "Epipen", "Sanitary Products", "Pain Relief", "Bandages", "Cough Syrup", "Allergy medication", "Indigestion", "Skincream"]
        self.table_new2 = ttk.Treeview(self.allocate_window, columns=new_columns2, show='headings', height=1)

        with setup_conn() as conn:
            # cursor = conn.cursor()
            # cursor.execute("SELECT glutenFree, dairyFree, noNuts, vegan, vegetarian, omnivore, epipen, sanitaryProducts, painRelief, bandages, coughsyrup, allergyMedication, indigestion, skincream FROM ressourcesOld where campID = ?", (selected_camp_id,))
            new_rows2 = self.r_res_two(selected_camp_id) # cursor.fetchall()
        for col in new_columns2:
            self.table_new2.heading(col, text=col)
            self.table_new2.column(col, width=100, anchor=CENTER)
        for row in new_rows2:
            self.table_new2.insert("", END, values=row)
            
        self.table_new2.pack(fill='x', padx=10, pady=10)

        self.category_entry = {}
        
        
        food_label = Label(self.allocate_window, text="Food Packets", font=("Helvetica", 12, "bold"))
        food_label.pack(fill='x')

        food_frame1 = Frame(self.allocate_window)
        food_frame1.pack(fill='x')
        
        for i, category in enumerate(food_categories1):
            label_cat = Label(food_frame1, text=f"{category}: ",  width=15)
            label_cat.pack(side='left')

            entry_var = StringVar()
            entry = Entry(food_frame1, textvariable=entry_var, width=10)
            entry.pack(side='left', padx=5)

            self.category_entry[category] = entry
            

        food_frame2 = Frame(self.allocate_window)
        food_frame2.pack(fill='x')
        
        for i, category in enumerate(food_categories2):
            label_cat = Label(food_frame2, text=f"{category}: ",  width=15)
            label_cat.pack(side='left')

            entry_var = StringVar()
            entry = Entry(food_frame2, textvariable=entry_var, width=10)
            entry.pack(side='left', padx=5)

            self.category_entry[category] = entry
            
        medicine_label = Label(self.allocate_window, text="Medicine", font=("Helvetica", 12, "bold"))
        medicine_label.pack(fill='x')

        medicine_frame1 = Frame(self.allocate_window)
        medicine_frame1.pack(fill='x')

        for i, category in enumerate(medicine_categories1):
            label_cat = Label(medicine_frame1, text=f"{category}: ", width=15)
            label_cat.pack(side='left')

            entry_var = StringVar()
            entry = Entry(medicine_frame1, textvariable=entry_var, width=10)
            entry.pack(side='left', padx=5)

            self.category_entry[category] = entry
        
        medicine_frame2 = Frame(self.allocate_window)
        medicine_frame2.pack(fill='x')
        
        for i, category in enumerate(medicine_categories2):
            label_cat = Label(medicine_frame2, text=f"{category}: ", width=15)
            label_cat.pack(side='left')

            entry_var = StringVar()
            entry = Entry(medicine_frame2, textvariable=entry_var, width=10)
            entry.pack(side='left', padx=5)

            self.category_entry[category] = entry

        update_button = Button(self.allocate_window, text="Update resources", command=self.update_resources)
        update_button.pack(pady=10)

    def update_resources(self):
        
        selected_camp_id = self.camp_id_var.get()
        selected_camp_id = int(selected_camp_id)
        print(selected_camp_id)

        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT planID FROM camps WHERE campID = ?''', (selected_camp_id,))
            hp_id = cursor.fetchone()
            print(selected_camp_id)
            print(self.camp_ids)
            if selected_camp_id not in [camp_id[0] for camp_id in self.camp_ids]:
                raise ValueError("Selected Camp ID does not exist. Please choose a valid Camp ID.")
            if hp_id:
                cursor.execute('SELECT * FROM ressourcesNew WHERE planID = ?', (hp_id[0],))
                existing_entry = cursor.fetchone()
                #print(existing_entry)

        valid = True
        class ExcError(Exception):
            pass
        
        for i in range(min(len(self.category_entry), len(existing_entry))):
            #print(i)
            category = list(self.category_entry.keys())[i]
            entry = self.category_entry[category]
            try:
                value = int(entry.get())
                #print(value)
                if value < 0:
                    valid = False
                    raise ValueError("Error: Input must be a positive integer")
                existing_value = existing_entry[i+1]
                if existing_value is not None:
                    result = existing_value - value
                    if result < 0:
                        valid = False
                        raise ExcError(f"Result of {existing_value} - {value} is negative.")
            except ValueError:
                Label(self.allocate_window, text="Error: Input must be a positive integer.").pack()
            except ExcError:
                Label(self.allocate_window, text=f"There are not enough resources to complete this allocation.").pack()
            
                

        category_values = {category: entry.get() for category, entry in self.category_entry.items()}
        category_values = {category: int(value) for category, value in category_values.items()}
        data = (selected_camp_id,)+ tuple(category_values.values())
        if valid:
            with setup_conn() as conn:
                cursor = conn.cursor()
                delete_from_table(cursor, 'ressourcesNew', data)
                update_table(cursor, 'ressourcesOld', data)
                conn.commit()
                self.allocate_window.destroy()
                self.refresh_tables()


    

    def refresh_tables(self):
        self.table_remaining.delete(*self.table_remaining.get_children())
        self.table_new.delete(*self.table_new.get_children())
        self.table_new.destroy()
        self.table_remaining.destroy()
        self.remaining_label.destroy()
        self.manage_r_button.destroy()
        self.camp_id_multiple.destroy()
        self.camp_id_l.destroy()

        new_columns = ["Humanitarian Plan", "GF",  "Dairy Free", "No nuts", "Vegan", "Vegetarian", "Other", "Epipen", "Sanitary Products", "Pain Relief", "Bandages", "Cough Syrup", "Allergy medication", "Indigestion", "Skincream"]
        self.table_new = ttk.Treeview(self.manage_resources, columns=new_columns, show='headings')
        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ressourcesNew")
            new_rows = cursor.fetchall()
        for col in new_columns:
            self.table_new.heading(col, text=col)
            self.table_new.column(col, width=100, anchor=CENTER)
        for row in new_rows:
            self.table_new.insert("", END, values=row)
        self.table_new.pack()
        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT campID FROM camps")
            self.camp_ids = cursor.fetchall()
            self.camp_id_var = StringVar()
            self.camp_id_multiple = ttk.Combobox(self.manage_resources, textvariable=self.camp_id_var, values=self.camp_ids, state='readonly')
            self.camp_id_multiple.set("Select the camp ID")
            self.camp_id_l = Label(self.manage_resources, text="Camp ID: ")
            self.camp_id_l.pack()
            self.camp_id_multiple.pack()
        # make message for any ressources that are low
        
        
        #displaying the remaining items
        #Label(self.manage_resources, text="").pack()
        self.remaining_label = Label(self.manage_resources, text="Remaining resources")
        self.remaining_label.pack()
        remaining_columns = ["Camp", "Humanitarian Plan", "Remaining Capacity", "Remaining GF", "Remaining Dairy Free", "Remaining No Nuts", "Remaining Vegan", "Remaining vegetarian", "Remaining Other", "Remaining Epipen", "Remaining sanitary products", "Remaining Pain Relief", " Remaining Bandages", "Remaining Cough Syrup", "Remaining Allergy medication", "Remaining Indigestion", "Remaining Skincream"]
        self.table_remaining = ttk.Treeview(self.manage_resources, columns= remaining_columns, show='headings')
        remaining_rows = remaining_resources()
        for col in remaining_columns:
            self.table_remaining.heading(col, text=col)
            self.table_remaining.column(col, width=100, anchor=CENTER)
        for row in remaining_rows:
            self.table_remaining.insert("", END, values=row)
        self.table_remaining.pack()

        self.manage_r_button = Button(self.manage_resources, text="Allocate ressources", command= self.allocate_ressources)
        self.manage_r_button.pack()

    def logout(self):
        refugee_gui.logout()
        self.master.destroy()
        self.login_window.master.destroy()
        window = Tk()
        frame = Frame(window, relief='sunken')
        window.geometry("+100+100")
        loginWindow(window, frame, handle_result)


class loginWindow:
    def __init__(self, master, frame, login_callback):
        self.master = master
        self.master.geometry("300x250")
        self.master.title("Login Window")

        self.frame = frame
        self.frame.grid(sticky="n")
        # Make the frame sticky for every case
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Make the window sticky for every case
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # self.frame = Frame(self.master, bg="#333333")
        # self.frame.grid(row=0,column=2, columnspan=3)

        # self.master.configure(bg = "#333333")
        Label(text=" ").grid(row=1, column=1, columnspan=3)
        self.login_button = Button(self.frame, text="Login", height="2", width="30", command=self.show_login)
        self.login_button.grid(row=3, column=1, columnspan=2, sticky="news", pady=20)
        Label(text="").grid(row=4, column=1, columnspan=2)
        self.exit_button = Button(self.frame, text="Exit", height="2", width="30", command=self.on_exit_click)
        self.exit_button.grid(row=5, column=1, columnspan=2)

        self.login_callback = login_callback
        self.login_result = StringVar()
        self.role_var = StringVar()
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.username_label = Label(self.frame, text="Username")
        self.username_entry = Entry(self.frame, textvariable=self.username_var)
        self.password_label = Label(self.frame, text="Password:")
        self.password_entry = Entry(self.frame, textvariable=self.password_var, show="*")
        self.role_var.set("volunteer")
        self.volunteer_radio = Radiobutton(self.frame, text="Volunteer", variable=self.role_var, value="volunteer")
        self.volunteer_radio.grid(row=2, column=0, columnspan=2)
        self.admin_radio = Radiobutton(self.frame, text="Admin", variable=self.role_var, value="admin")
        self.admin_radio.grid(row=2, column=2, columnspan=2)
        self.previous_state = None

    def show_login(self):
        self.result = self.role_var.get()
        self.previous_state = {
            "login_button": self.login_button.grid_info(),
            "exit_button": self.exit_button.grid_info(),
            "admin_radio": self.admin_radio.grid_info(),
            "volunteer_radio": self.volunteer_radio.grid_info(),
        }

        self.login_button.grid_remove()
        self.exit_button.grid_remove()
        self.admin_radio.grid_remove()
        self.volunteer_radio.grid_remove()

        self.username_label.grid(row=2, column=0)
        self.username_entry.grid(row=2, column=1)
        self.password_label.grid(row=3, column=0)
        self.password_entry.grid(row=3, column=1)

        if self.result == "volunteer":
            self.type_login_label = Label(self.frame, text="Welcome to the volunteer login")
            self.type_login_label.grid(row=1, column=0, columnspan=3)

            self.login2_button = Button(self.frame, text="Login", command=self.volunteer_login)
            self.login2_button.grid(row=4, column=0, columnspan=2)
        else:
            self.type_login_label = Label(self.frame, text="Welcome to the admin login")
            self.type_login_label.grid(row=1, column=0, columnspan=3)

            self.login_button = Button(self.frame, text="Login", command=self.admin_login)
            self.login_button.grid(row=4, column=0, columnspan=2)

        self.back_button = Button(self.frame, text="Go back", command=self.go_back)
        self.back_button.grid(row=5, column=0, columnspan=2)


    def go_back(self):
        self.master.destroy()
        window = Tk()
        frame = Frame(window, relief='sunken')
        window.geometry("+100+100")
        loginWindow(window, frame, handle_result)
        '''
        # Remove the login widgets that are common to both roles
        self.username_label.grid_remove()
        self.username_entry.grid_remove()
        self.password_label.grid_remove()
        self.password_entry.grid_remove()
        self.type_login_label.grid_remove()
        self.back_button.grid_remove()

        # Remove the specific login button for each role
        if self.result == "volunteer":
            self.login2_button.grid_remove()
        else:
            self.login_button.grid_remove()

        # Restore the initial state of the window
        self.login_button.grid(**self.previous_state["login_button"])
        self.exit_button.grid(**self.previous_state["exit_button"])
        self.admin_radio.grid(**self.previous_state["admin_radio"])
        self.volunteer_radio.grid(**self.previous_state["volunteer_radio"])

        # Clear the previous state if no longer needed
        self.previous_state = None'''

    def volunteer_login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        with setup_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result is not None and result[0] == username:
                cursor.execute("SELECT status FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()

                if result[0] == 'active':
                    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
                    result = cursor.fetchone()
                    if result[0] == password:
                        self.master.withdraw()
                        tk.messagebox.showinfo("Succeess", "You have successfully logged as volunteer"
                                                           "\nClick OK to proceed")

                        successful_login_label = Label(self.frame, text="Successful Login")
                        successful_login_label.grid(row=6, column=0, columnspan=3)
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
                        self.open_volunteer_menu(username, password, session)

                    else:
                        '''
                        unsuccessful_login_label = Label(self.frame, text="Incorrect password")
                        unsuccessful_login_label.grid(row=7, column=0, columnspan=3)
                        '''
                        tk.messagebox.showinfo("Error", "Incorrect password")
                else:
                    '''
                    account_deactivated = Label(self.frame, text="Your account has been deactivated")
                    account_deactivated.grid(row=7, column=0, columnspan=3)
                    '''
                    tk.messagebox.showinfo("Error", "Your account has been deactivated")
            else:
                '''
                account_not_found = Label(self.frame, text="Volunteer not found")
                account_not_found.grid(row=7, column=0, columnspan=3)
                '''
                tk.messagebox.showinfo("Volunteer not found", "Volunteer not found")

    def open_volunteer_menu(self, username, password, session):
        self.open_volunteer_menu = Toplevel(self.master)
        volunteerWindow(self.open_volunteer_menu, username, password, session, self)

    def open_admin_menu(self):
        self.open_admin_menu = Toplevel(self.master)
        adminWindow(self.open_admin_menu, self)

    def admin_login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if username == 'admin' and password == "111":
            self.master.withdraw()
            tk.messagebox.showinfo("Succeess", "You have successfully logged as admin"
                                               "\nClick OK to proceed")
            successful_login_label = Label(self.frame, text="Successful Login")
            successful_login_label.grid(row=6, column=0, columnspan=3)
            self.open_admin_menu()
        elif username != 'admin':
            '''
            wrong_username = Label(self.frame, text="Incorrect username")
            wrong_username.grid(row=6, column=0, columnspan=3)
            '''
            tk.messagebox.showinfo("Incorrect username", "Incorrect username")
        elif password != '111':
            '''
            wrong_password = Label(self.frame, text="Incorrect password")
            wrong_password.grid(row=6, column=0, columnspan=3)
            '''
            tk.messagebox.showinfo("Incorrect password", "Incorrect")

    def on_login_click(self):
        result = self.role_var.get()
        username = self.username_var.get()
        password = self.password_var.get()
        if self.login_callback:
            self.login_callback(result, username, password)

    def on_exit_click(self):
        self.master.destroy()
        print("Exit")
        

def handle_result(result, username, password):
    print("Login Result: ", result)
    print("Username: ", username)
    print("Password: ", password)


def create_user_session(user_data):
    # Function to create a user session
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


window = Tk()
frame = Frame(window, relief='sunken')
window.geometry("+100+100")

login_window = loginWindow(window, frame, handle_result)
# window.title("Login form")
# window.geometry("340x440")
# window.configure(bg = "#333333")


# #creating widgets
# login_label = Label(window, text = "Login")
# username_label = 


window.mainloop()
