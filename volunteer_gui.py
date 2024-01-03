'''from refugee_gui import *


def open_refugee_menu():
    refugee_menu()


def view_volunteer_info():
    view_info_menu = tk.Toplevel()
    view_info_menu.title('View Volunteer Information')
    view_info_menu.geometry('400x400')


def edit_volunteer_info():
    edit_info_menu = tk.Toplevel()
    edit_info_menu.title('Edit Volunteer Information')
    edit_info_menu.geometry('400x400')


def manage_volunteer_schedule():
    schedule_menu = tk.Toplevel()
    schedule_menu.title('Manage Volunteer Schedule')
    schedule_menu.geometry('400x400')


def volunteer_menu():
    root = tk.Tk()
    root.title("Volunteer Menu")
    root.geometry("400x400")

    view_volunteer_info_button = tk.Button(root, text="Volunteer Info", command=view_volunteer_info)
    view_volunteer_info_button.pack(pady=10)

    edit_volunteer_info_button = tk.Button(root, text="Edit Volunteer Info", command=edit_volunteer_info)
    edit_volunteer_info_button.pack(pady=10)

    manage_refugee_button = tk.Button(root, text="Manage Refugee", command=open_refugee_menu)
    manage_refugee_button.pack(pady=10)

    manage_schedule_button = tk.Button(root, text="Manage Schedule", command=manage_volunteer_schedule)
    manage_schedule_button.pack(pady=10)

    root.mainloop()


volunteer_menu()'''
