import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from hpava import *
from fcamp import *
import re

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


class User:
    def __init__(self, username: str, password: str, name: str, surname: str, phone: str, campID: int, availability: str, user_type: str, status: str):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.phone = phone
        self.campID = campID
        self.availability = availability
        self.user_type = user_type
        self.status = status
    
    def create_volunteer(self):
        with setup_conn() as conn:
            cursor = conn.cursor()
            data = (self.username, self.password, self.name, self.surname, self.phone, self.campID, self.availability, self.user_type, self.status)
            insert_query(cursor, 'users', data)
            conn.commit()
            

def update_count(camp_id): # this updates volunteerNo in camps table, needs to be called after create and delete v
    
    count_query = "SELECT COUNT(*) FROM users WHERE campID = ?"
    cursor.execute(count_query, (camp_id,))
    count_result = cursor.fetchone()[0]

    update_query = "UPDATE camps SET totalVolunteers = ? WHERE campID = ?"
    cursor.execute(update_query, (count_result, camp_id))
    conn.commit() 

def get_campid(user_id):
        
        query = "SELECT campID FROM users WHERE userID = ?"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0]
    
    
def create_v(parent):
    create_menu = tk.Toplevel(parent)
    create_menu.title("Create Volunteer")
    create_menu.geometry("1500x800")
    
    
    def available_campids():
        
        # Query to fetch plan IDs where end_date is null
        query = "SELECT campID FROM camps WHERE status = 'Active'"
        cursor.execute(query)

        # Fetch all rows from the query
        rows = cursor.fetchall()

        # Extracting plan IDs from rows
        camp_ids = [row[0] for row in rows]
        return camp_ids
    
    camp_ids = available_campids()
    
    # camp ID
    campIdLabel = tk.Label(create_menu, text="Enter camp ID: ")
    campIdLabel.grid(row=1, column=0)
    campIdCombo = ttk.Combobox(create_menu, values=camp_ids, state="readonly")
    campIdCombo.grid(row=1, column=1)
    campid_error_label = tk.Label(create_menu, text="", fg="red")
    campid_error_label.grid(row=1, column=2)
    
    # Username
    username_label = tk.Label(create_menu, text="Username (5 - 20): ")
    username_label.grid(row=3, column=0)
    username_entry = tk.Entry(create_menu)
    username_entry.grid(row=3, column=1)
    username_error_label = tk.Label(create_menu, text="", fg="red")
    username_error_label.grid(row=3, column=2)

    # Password
    password_label = tk.Label(create_menu, text="Password (3 - 15): ")
    password_label.grid(row=5, column=0)
    password_entry = tk.Entry(create_menu, show="*")
    password_entry.grid(row=5, column=1)
    password_error_label = tk.Label(create_menu, text="", fg="red")
    password_error_label.grid(row=5, column=2)

    # Name
    name_label = tk.Label(create_menu, text="Name: ")
    name_label.grid(row=7, column=0)
    name_entry = tk.Entry(create_menu)
    name_entry.grid(row=7, column=1)
    name_error_label = tk.Label(create_menu, text="", fg="red")
    name_error_label.grid(row=7, column=2)

    # Surname
    surname_label = tk.Label(create_menu, text="Surname: ")
    surname_label.grid(row=9, column=0)
    surname_entry = tk.Entry(create_menu)
    surname_entry.grid(row=9, column=1)
    surname_error_label = tk.Label(create_menu, text="", fg="red")
    surname_error_label.grid(row=9, column=2)

    # Phone
    phone_label = tk.Label(create_menu, text="Phone: ")
    phone_label.grid(row=11, column=0)
    phone_entry = tk.Entry(create_menu)
    phone_entry.grid(row=11, column=1)
    phone_error_label = tk.Label(create_menu, text="", fg="red")
    phone_error_label.grid(row=11, column=2)

    # Availability
    availability_label = tk.Label(create_menu, text="Availability: ")
    availability_label.grid(row=13, column=0)
    availability_options = ["full-time", "part-time"]
    availability_combo = ttk.Combobox(create_menu, values=availability_options, state="readonly")
    availability_combo.grid(row=13, column=1)
    availability_error_label = tk.Label(create_menu, text="", fg="red")
    availability_error_label.grid(row=13, column=2)

    def is_valid_string(input_string):
        return bool(re.fullmatch(r"[A-Za-z\s]+", input_string))


    def is_valid_username(username):
        if len(username)>4 and len(username)<21:
            return True
        else:
            return False


    def is_valid_name(name):
        return is_valid_string(name)
    
    
    def is_valid_surname(surname):
        return is_valid_string(surname)
    
    
    def is_valid_phone(phone):
        pattern = r"^\+\d{1,14}$"
        return bool(re.match(pattern, phone))
    
    
    def is_valid_password(password):
        if len(password)>2 and len(password)<16:
            return True
        else:
            return False

    
    
    def submit_form():
        
        input_campid = campIdCombo.get()
        input_username = username_entry.get()
        input_password = password_entry.get()
        input_name = name_entry.get()
        input_surname = surname_entry.get()
        input_phone = phone_entry.get()
        input_availability = availability_combo.get()
        
        
        
        
        
        valid = True
        # Validate the inputs
        if not is_valid_username(input_username):
            username_error_label.config(text="Invalid username", fg="red")
            valid = False
        else:
            username_error_label.config(text="")

        if not is_valid_password(input_password):
            password_error_label.config(text="Invalid password", fg="red")
            valid = False
        else:
            password_error_label.config(text="")

        if not is_valid_name(input_name):
            name_error_label.config(text="Invalid name", fg="red")
            valid = False
        else:
            name_error_label.config(text="")
            
        if not is_valid_surname(input_surname):
            surname_error_label.config(text="Invalid surname", fg="red")
            valid = False
        else:
            surname_error_label.config(text="")
            
        if not is_valid_phone(input_phone):
            phone_error_label.config(text="Invalid phone", fg="red")
            valid = False 
        else:
            phone_error_label.config(text="")
            
        result = False
        
        if valid:
            newvolunteer = User(input_username, input_password, input_name, input_surname, input_phone, input_campid, input_availability, 'volunteer', 'active')
            result = newvolunteer.create_volunteer()
            update_count(input_campid)
        

        if result is not False:
            tk.messagebox.showinfo("Success", "Volunteer created") 
        else:
            tk.messagebox.showinfo("Failed", "Failed to create a new volunteer")

    submitBtn = tk.Button(create_menu, text="Create volunteer", command=submit_form)
    submitBtn.grid(row=15, column=0, columnspan=2)
    
    # back to the main menu
    exitBtn = tk.Button(create_menu, text="Exit", command=create_menu.destroy)
    exitBtn.grid(row=17, column=0, columnspan=2)


def view_vs(parent):
    
    # sql
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    # window title
    users_window = tk.Toplevel(parent)
    users_window.title("All users")
    users_window.geometry("1500x800")

    columns = ('UserID', 'Username', 'Password', 'Name', 'Surname', 'Phone', 'Camp ID', 'Availability', 'User Type', 'Status')
    tree = ttk.Treeview(users_window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col.title())
        tree.column(col, width=100)

    for user in users:
        tree.insert('', tk.END, values=user)

    tree.pack(expand=True, fill='both')
    
    # back to the main menu
    back_button = tk.Button(users_window, text="Back to Main Menu", command=users_window.destroy)
    back_button.pack()
    tableExp = tk.Label(users_window, text="This table shows all volunteers registered with the application.") 
    tableExp.pack(side="bottom", pady=10)


def view_v(parent):
    def show_volunteer():
        # clear
        for i in tree.get_children():
            tree.delete(i)
        
        v_id = v_id_entry.get()
        if not v_id.isdigit():
            result_label.config(text="Please enter a valid volunteerID.")
            return
        
        # sql
        query = "SELECT * FROM users WHERE userID = ?"
        cursor.execute(query, (v_id,))
        volunteer = cursor.fetchone()
        
        # success messages
        if volunteer:
            tree.insert('', tk.END, values=volunteer)
            result_label.config(text="")
        else:
            result_label.config(text="No volunteer found with that ID.")

    # title window
    v_window = tk.Toplevel(parent)
    v_window.title("View Volunteers by ID")
    v_window.geometry("1500x800")

    instruction_label = tk.Label(v_window, text="Which volunteerID do you want to see?")
    instruction_label.pack()

    v_id_entry = tk.Entry(v_window)
    v_id_entry.pack()

    submit_button = tk.Button(v_window, text="Submit", command=show_volunteer)
    submit_button.pack()

    result_label = tk.Label(v_window, text="")
    result_label.pack()

    columns = ('UserID', 'Username', 'Password', 'Name', 'Surname', 'Phone', 'Camp ID', 'Availability', 'User Type', 'Status')

    tree = ttk.Treeview(v_window, columns=columns, show='headings', height=1)
    for col in columns:
        tree.heading(col, text=col.title())
        tree.column(col, width=100)
    tree.pack()
    
    # back to the main menu
    back_button = tk.Button(v_window, text="Back to Manage Volunteers Menu", command=v_window.destroy)
    back_button.pack()


def edit_v(parent):
    
    def fetch_v():
        # clear
        for i in tree.get_children():
            tree.delete(i)
        for widget in edit_area.winfo_children():
            widget.destroy()

        # input and save vID
        v_id = v_id_entry.get()
        if not v_id.isdigit():
            result_label.config(text="Please enter a valid volunteerID.")
            return
        
        # sql
        query = "SELECT * FROM users WHERE userID = ?"
        cursor.execute(query, (v_id,))
        volunteer = cursor.fetchone()
        
        if volunteer:
            tree.insert('', tk.END, values=volunteer)
            result_label.config(text="")
            create_edit_interface()
        else:
            result_label.config(text="No volunteer found with that ID.")
    
    def create_edit_interface(): #what for
        category_label = tk.Label(edit_area, text="Which category do you want to edit?")
        category_label.pack()
        
        categories = ('Name', 'Surname', 'Phone', 'Availability')
        category_combo = ttk.Combobox(edit_area, values=categories, state="readonly")
        category_combo.pack()
        
        def category_selected(event=None):
            # Clear previous inputs and buttons
            for widget in input_area.winfo_children():
                widget.destroy()

            category = category_combo.get().lower()  # Convert to lower case for comparison

            # Create appropriate input widget and save button
            if category in ['availability']:
                options = {
                    'availability': ["full-time", "part-time"]
                }
                new_value_combo = ttk.Combobox(input_area, values=options[category], state="readonly")
                new_value_combo.pack()
                save_button = tk.Button(input_area, text="Save", command=lambda: update_v(category, new_value_combo.get()))
            else:  # For 'name', 'surname', 'phone'
                new_value_entry = tk.Entry(input_area)
                new_value_entry.pack()
                save_button = tk.Button(input_area, text="Save", command=lambda: update_v(category, new_value_entry.get()))

            save_button.pack()
        
        category_combo.bind('<<ComboboxSelected>>', category_selected)
        
        
    def is_valid_string(input_string):
        return bool(re.fullmatch(r"[A-Za-z\s]+", input_string))

    # def is_valid_name(name):
    #     return is_valid_string(name)
    
    # def is_valid_surname(surname):
    #     return is_valid_string(surname)
    
    def is_valid_phone(phone):
        pattern = r"^\+\d{1,14}$"
        return bool(re.match(pattern, phone))
    
    def update_v(category, new_value):
        
        error_message = ""
        valid = True

        if category.lower() == 'name' and not is_valid_string(new_value):
            valid = False
            error_message = "Invalid name. Name cannot contain numbers."

        if category.lower() == 'surname' and not is_valid_string(new_value):
            valid = False
            error_message = "Invalid surname. Surname cannot contain numbers."

        if category.lower() == 'phone' and not is_valid_phone(new_value):
            valid = False
            error_message = "Invalid phone number. Please enter a valid phone number."

        if valid:
            v_id = v_id_entry.get()
            query = f"UPDATE users SET {category} = ? WHERE userID = ?"
            cursor.execute(query, (new_value, v_id))
            conn.commit()
            result_label.config(text=f"Volunteer {v_id} updated: {category} set to {new_value}.")
            fetch_v()  # Refresh the view
        else:
            result_label.config(text=error_message, foreground="red")

    # title window
    edit_window = tk.Toplevel(parent)
    edit_window.title("Edit Volunteer")
    edit_window.geometry("1500x800")

    tk.Label(edit_window, text="Enter the volunteerID of the volunteer you want to edit:").pack()
    # v_id_entry = tk.Entry(edit_window)
    # v_id_entry.pack()
    
    # menu for user ID
    cursor.execute("SELECT userID FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    selected_user_id = tk.StringVar()
    v_id_entry = ttk.Combobox(edit_window, textvariable=selected_user_id, values=user_ids, state="readonly")
    v_id_entry.pack()

    submit_button = tk.Button(edit_window, text="Fetch Volunteer", command=fetch_v)
    submit_button.pack()

    result_label = tk.Label(edit_window, text="")
    result_label.pack()

    columns = ('UserID', 'Username', 'Password', 'Name', 'Surname', 'Phone', 'Camp ID', 'Availability', 'User Type', 'Status')
    tree = ttk.Treeview(edit_window, columns=columns, show='headings', height=1)
    for col in columns:
        tree.heading(col, text=col.title())
    tree.pack()

    edit_area = tk.LabelFrame(edit_window, text="Edit Area")
    edit_area.pack(fill="x", expand="yes")

    input_area = tk.LabelFrame(edit_window, text="Input Area")
    input_area.pack(fill="x", expand="yes")
    
    # back to the main menu
    back_button = tk.Button(edit_window, text="Back to Manage Volunteers Menu", command=edit_window.destroy)
    back_button.pack()

def da_v(parent):
    
    def refresh_table(tree, cursor):
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT userID, username, status FROM users")
        for volunteer in cursor.fetchall():
            tree.insert('', tk.END, values=volunteer)

    def update_status(v_id, cursor, conn, tree):
        cursor.execute("SELECT status FROM users WHERE userID = ?", (v_id,))
        current_status = cursor.fetchone()[0]
        new_status = "inactive" if current_status == "active" else "active"
        cursor.execute("UPDATE users SET status = ? WHERE userID = ?", (new_status, v_id))
        conn.commit()
        refresh_table(tree, cursor)
    
    edit_window = tk.Toplevel(parent)
    edit_window.title("Activate/deactivate Volunteer")
    edit_window.geometry("1500x800")

    columns = ('UserID', 'Username', 'Status')
    tree = ttk.Treeview(edit_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col.title())
    tree.pack(expand=True, fill='both')

    cursor = conn.cursor()
    refresh_table(tree, cursor)

    # Dropdown menu for user ID
    cursor.execute("SELECT userID FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    selected_user_id = tk.StringVar()
    user_id_dropdown = ttk.Combobox(edit_window, textvariable=selected_user_id, values=user_ids, state="readonly")
    user_id_dropdown.pack()

    def on_user_id_select():
        v_id = selected_user_id.get()
        update_status(v_id, cursor, conn, tree)

    # Activate/Deactivate Button
    act_deact_button = tk.Button(edit_window, text="Activate/Deactivate", command=on_user_id_select)
    act_deact_button.pack()

    # Back to main menu button
    back_button = tk.Button(edit_window, text="Back", command=edit_window.destroy)
    back_button.pack()



def delete_v(parent):
    def delete_volunteer():
        # input and save vID
        v_id = v_id_entry.get()
        if not v_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid volunteerID.")
            return
        
        camp_id = get_campid(v_id)
        
        # sql
        cursor.execute("DELETE FROM users WHERE userID = ?", (v_id,))
        conn.commit()
        
        # success messages
        if cursor.rowcount == 0:
            messagebox.showinfo("Not found", f"No volunteer found with ID {v_id}.")
        else:
            messagebox.showinfo("Success", f"Volunteer with ID {v_id} has been deleted.")
            update_count(camp_id)
            refresh_treeview()
    
    def refresh_treeview():
        # clear for later refreshing
        for i in tree.get_children():
            tree.delete(i)
            
        cursor.execute("SELECT * FROM users")
        vs = cursor.fetchall()
        
        for v in vs:
            tree.insert('', tk.END, values=v)

    
    # title window
    dp_window = tk.Toplevel(parent)
    dp_window.title("Delete Volunteer by ID")
    dp_window.geometry("1500x800")

    instruction_label = tk.Label(dp_window, text="Enter the volunteerID of the plan you want to delete:")
    instruction_label.pack()

    v_id_entry = tk.Entry(dp_window)
    v_id_entry.pack()

    submit_button = tk.Button(dp_window, text="Delete Volunteer", command=delete_volunteer)
    submit_button.pack()
    

    columns = ('UserID', 'Username', 'Password', 'Name', 'Surname', 'Phone', 'Camp ID', 'Availability', 'User Type', 'Status')

    tree = ttk.Treeview(dp_window, columns=columns, show='headings', height=10)
    for col in columns:
        tree.heading(col, text=col.title())
    refresh_treeview()
    
    tree.pack(expand=True, fill='both')
    
    # back to the main menu
    back_button = tk.Button(dp_window, text="Back to Manage Volunteers Menu", command=dp_window.destroy)
    back_button.pack()


def volunteer_menu(parent):
    create_v_button = tk.Button(parent, text="Create new volunteer", command=lambda: create_v(parent))
    create_v_button.pack(pady=10)

    view_vs_button = tk.Button(parent, text="View all volunteers", command=lambda: view_vs(parent))
    view_vs_button.pack(pady=10)

    view_v_button = tk.Button(parent, text="View a specific volunteer", command=lambda: view_v(parent))
    view_v_button.pack(pady=10)

    edit_v_button = tk.Button(parent, text="Edit volunteer personal information", command=lambda: edit_v(parent))
    edit_v_button.pack(pady=10)

    da_v_button = tk.Button(parent, text="Activate/deactivate volunteer", command=lambda: da_v(parent))
    da_v_button.pack(pady=10)

    delete_v_button = tk.Button(parent, text="Delete volunteer", command=lambda: delete_v(parent))
    delete_v_button.pack(pady=10)
