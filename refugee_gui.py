import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from unittest import case

from refugee import *
from family import *


open_windows = []

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def show_tip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="grey",  # Adjust the background color
                         foreground="white",  # Set text color to white
                         relief=tk.SOLID, borderwidth=1,
                         font=("TkDefaultFont", "8", "normal"))
        label.pack(ipadx=5, ipady=5)

    def hide_tip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def create_tooltip(widget, text):
    tool_tip = ToolTip(widget)
    def enter(event):
        tool_tip.show_tip(text)
    def leave(event):
        tool_tip.hide_tip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def delete_refugee():
    global open_windows
    delete_menu = tk.Tk()
    open_windows.append(delete_menu)
    delete_menu.title("Delete Refugee")
    delete_menu.geometry("400x400")

    IDLabel = tk.Label(delete_menu, text="Refugee ID: ")
    IDLabel.grid(row=0, column=0)

    IDEntry = tk.Entry(delete_menu)
    IDEntry.grid(row=0, column=1)

    def submit_form():
        refugeeId = int(IDEntry.get())
        result = Refugee.delete_refugee(refugeeId)
        if result == 2:
            update_count_ref()
            tk.messagebox.showinfo("Success", "Refugee deleted")
        elif result == 1:
            tk.messagebox.showinfo("Failed", "Failed to delete refugee")
        elif result == 3:
            tk.messagebox.showinfo("Failed", "Refugee does not exist")

    submitBtn = tk.Button(delete_menu, text="Delete Refugee", command=submit_form)
    submitBtn.grid(row=1, column=0, columnspan=2)


def health_word_to_score(value):
    if value == "Excellent":
        return 5
    elif value == "Good":
        return 4
    elif value == "Moderate":
        return 3
    elif value == "Fair":
        return 2
    elif value == "Poor":
        return 1


def health_score_to_word(value):
    if value == 5:
        return "Excellent"
    elif value == 4:
        return "Good"
    elif value == 3:
        return "Moderate"
    elif value == 2:
        return "Fair"
    elif value == 1:
        return "Poor"
    else:
        return value


def generate_new_family():
    familyList = get_family()
    famIDInt = [int(familyID) for familyID in familyList]
    currentFamilyID = max(famIDInt)
    newFamilyID = currentFamilyID + 1
    return str(newFamilyID)


def get_camp():
    campList = []
    with setup_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT campID FROM camps")
        familyIDs = cursor.fetchall()
        for familyID in familyIDs:
            if str(familyID[0]) not in campList:
                campList.append(str(familyID[0]))
    return campList


def update_count_ref():
    campList = get_camp()
    for campID in campList:
        with setup_conn() as conn:
            cursor = conn.cursor()
            column_mapping = {
                            "glutenFree": "totalGF",
                            "dairyFree": "totalDF",
                            "noNuts": "totalNN",
                            "vegan": "totalVgn",
                            "vegetarian": "totalVgt",
                            "omnivore": "totalOmn",
                            #"epipen": "totalEP"
                            "sanitaryProducts" : "totalSP"        
            }            
            camps_columns = []
            for refugee_column, camps_column in column_mapping.items():
                count_query = f"SELECT COUNT(*) FROM refugee WHERE campID=? AND {refugee_column}=?"
                counts = cursor.execute(count_query, (campID, True)).fetchone()[0]
                camps_columns.append((camps_column, counts))
            
            count_query = "SELECT COUNT(*) FROM refugee WHERE campID = ?"
            cursor.execute(count_query, (campID,))
            total_refugee = cursor.fetchone()[0]

            update_query = "UPDATE camps SET totalRefugees = ? WHERE campID = ?"
            cursor.execute(update_query, (total_refugee, campID))

            for camps_column, count in camps_columns:
                update_query = f"UPDATE camps SET {camps_column}=? WHERE campID=?"
                cursor.execute(update_query, (count, campID))

            conn.commit()


def update_count_vol():
    campList = get_camp()
    for campID in campList:
        with setup_conn() as conn:
            cursor = conn.cursor()
            count_query = "SELECT COUNT(*) FROM users WHERE campID = ?"
            cursor.execute(count_query, (campID,))
            count_result = cursor.fetchone()[0]

            update_query = "UPDATE camps SET totalRefugees = ? WHERE campID = ?"
            cursor.execute(update_query, (count_result, campID))
            conn.commit()


def create_refugee():
    global open_windows
    create_menu = tk.Tk()
    open_windows.append(create_menu)
    create_menu.title("Create Refugee")
    create_menu.geometry("1100x500")

    nameLabel = tk.Label(create_menu, text="Refugee name: ")
    nameLabel.grid(row=0, column=0)
    nameEntry = tk.Entry(create_menu)
    nameEntry.grid(row=0, column=1)

    surnameLabel = tk.Label(create_menu, text="Refugee surname: ")
    surnameLabel.grid(row=0, column=2)
    surnameEntry = tk.Entry(create_menu)
    surnameEntry.grid(row=0, column=3)

    cIDOptions = get_camp()
    cIDLabel = tk.Label(create_menu, text="Refugee camp ID: ")
    cIDLabel.grid(row=1, column=0)
    cIDDL = ttk.Combobox(create_menu, values=cIDOptions, state="readonly")
    cIDDL.grid(row=1, column=1)

    ageLabel = tk.Label(create_menu, text="Refugee age: ")
    ageLabel.grid(row=1, column=2)
    ageEntry = tk.Entry(create_menu)
    ageEntry.grid(row=1, column=3)

    lanOptions = ["Chinese","Spanish","English","Hindi","Arabic","Bengali","Portuguese","Russian","Urdu","Other"]
    lanLabel = tk.Label(create_menu, text="Refugee languages: ")
    lanLabel.grid(row=2, column=0)
    lanEntry = ttk.Combobox(create_menu, values=lanOptions, state='readonly')
    lanEntry.grid(row=2, column=1)

    genOptions = ['Male', 'Female', 'Others']
    genLabel = tk.Label(create_menu, text="Refugee gender: ")
    genLabel.grid(row=2, column=2)
    genDL = ttk.Combobox(create_menu, values=genOptions, state='readonly')
    genDL.grid(row=2, column=3)

    BTOptions = ["A+", "A-", "AB+", "AB-", "B+", "B-", "O+", "O-"]
    BTLabel = tk.Label(create_menu, text="Refugee blood type: ")
    BTLabel.grid(row=3, column=0)
    BTDL = ttk.Combobox(create_menu, values=BTOptions, state='readonly')
    BTDL.grid(row=3, column=1)

    healthOptions = ['Excellent', 'Good', 'Moderate', 'Fair', 'Poor']
    psyHLabel = tk.Label(create_menu, text="Refugee psychological health: ")
    psyHLabel.grid(row=3, column=2)
    psyHDL = ttk.Combobox(create_menu, values=healthOptions, state='readonly')
    psyHDL.grid(row=3, column=3)

    phyHLabel = tk.Label(create_menu, text="Refugee physical health: ")
    phyHLabel.grid(row=4, column=0)
    phyHDL = ttk.Combobox(create_menu, values=healthOptions, state='readonly')
    phyHDL.grid(row=4, column=1)

    familyList = get_family()
    fIDOptions = familyList
    fIDOptions.append('Generate new family ID')
    fIDLabel = tk.Label(create_menu, text="Refugee family ID: ")
    fIDLabel.grid(row=4, column=2)
    fIDDL = ttk.Combobox(create_menu, values=fIDOptions, state='readonly')
    fIDDL.grid(row=4, column=3)

    dietOptions = ['Gluten Free', 'Dairy Free', 'No Nuts', 'Vegan', 'Vegetarian', 'Omnivore', 'None']
    dietLabel = tk.Label(create_menu, text="Diet options: ")
    dietLabel.grid(row=5, column=1)
    dRDL = ttk.Combobox(create_menu, values=dietOptions, state='readonly')
    dRDL.grid(row=5, column=2)
    dRDL.set('None')

    def diet_options(choice, gF = False, dF = False, nN = False, Vegan = False, Vege = False, Omnivore = False,
                     none = False):
        match choice:
            case 'Gluten Free':
                gF = True
            case 'Dairy Free':
                dF = True
            case 'No Nuts':
                nN = True
            case 'Vegan':
                Vegan = True
            case 'Vegetarian':
                Vege = True
            case 'Omnivore':
                Omnivore = True
            case 'None':
                none = True
        return gF, dF, nN, Vegan, Vege, Omnivore, none

    medicalLabel = tk.Label(create_menu, text="If you need the following resources please choose yes: ")
    medicalLabel.grid(row=7, column=1)

    question_mark = tk.Label(create_menu, text="?", font=("Arial", 12, "bold"), cursor="question_arrow",
                             relief=tk.RAISED, borderwidth=2, width=2, height=1)
    question_mark.grid(row=7, column=2)

    create_tooltip(question_mark, "If they are unsure, click yes to the question above and return back.")

    epiLabel = tk.Label(create_menu, text="Epipen: ")
    epiLabel.grid(row=10, column=0)
    epi = tk.BooleanVar(value=False)
    epiTBtn = tk.Radiobutton(create_menu, text="Yes", variable=epi, value=True)
    epiTBtn.grid(row=10, column=1)
    epiFBtn = tk.Radiobutton(create_menu, text="No", variable=epi, value=False)
    epiFBtn.grid(row=10, column=2)

    pRLabel = tk.Label(create_menu, text="Plain relief: ")
    pRLabel.grid(row=11, column=0)
    pR = tk.BooleanVar(value=False)
    pRTBtn = tk.Radiobutton(create_menu, text="Yes", variable=pR, value=True)
    pRTBtn.grid(row=11, column=1)
    pRFBtn = tk.Radiobutton(create_menu, text="No", variable=pR, value=False)
    pRFBtn.grid(row=11, column=2)

    bLabel = tk.Label(create_menu, text="Bandages: ")
    bLabel.grid(row=12, column=0)
    bandages = tk.BooleanVar(value=False)
    bTBtn = tk.Radiobutton(create_menu, text="Yes", variable=bandages, value=True)
    bTBtn.grid(row=12, column=1)
    bFBtn = tk.Radiobutton(create_menu, text="No", variable=bandages, value=False)
    bFBtn.grid(row=12, column=2)

    sPLabel = tk.Label(create_menu, text="Sanitary products: ")
    sPLabel.grid(row=13, column=0)
    sP = tk.BooleanVar(value=False)
    sPTBtn = tk.Radiobutton(create_menu, text="Yes", variable=sP, value=True)
    sPTBtn.grid(row=13, column=1)
    sPFBtn = tk.Radiobutton(create_menu, text="No", variable=sP, value=False)
    sPFBtn.grid(row=13, column=2)

    def on_yes_button_click():
        global symptom_window, recommendation_window
        show_symptoms_page()

    def on_no_button_click():
        pass

    symptoms = ["Pain", "Inflammation", "Cough", "Fever", "Allergic Reaction", "Indigestion", "Itchy Skin"]
    symptoms_vars = []
    symptom_window = None
    recommendation_window = None

    medicalAssisstancelabel = tk.Label(create_menu, text="Does the refugee require medical assistance?")
    medicalAssisstancelabel.grid(row=6, column=0)
    yesButton = tk.Button(create_menu, text="Yes", command=on_yes_button_click)
    yesButton.grid(row=6, column=1)
    noButton = tk.Button(create_menu, text="No", command=on_no_button_click)
    noButton.grid(row=6, column=2)

    def show_symptoms_page():
        symptoms_page()

    def symptoms_page():
        global symptoms_vars, other_var, symptom_window
        symptoms_vars = [tk.IntVar() for _ in symptoms]

        symptom_window = tk.Toplevel()
        symptom_window.title("Symptom Table")
        symptom_window.geometry("1100x500")


        symptom_window.grid_rowconfigure(0, weight=1)
        for i in range(len(symptoms) + 2):
            symptom_window.grid_rowconfigure(i + 1, weight=1)
        symptom_window.grid_columnconfigure(0, weight=1)
        symptom_window.grid_columnconfigure(1, weight=1)

        message_label = tk.Label(symptom_window,
                                 text="Please check the box if they only have these symptoms otherwise, click 'Other'.")
        message_label.grid(row=0, column=0, columnspan=2, pady=20)

        labels = [tk.Label(symptom_window, text=symptom) for symptom in symptoms]
        check_buttons = [tk.Checkbutton(symptom_window, variable=symptom_var) for symptom_var in symptoms_vars]

        for i, (label, check_button) in enumerate(zip(labels, check_buttons)):
            label.grid(row=i + 1, column=0, padx=10, pady=10, sticky=tk.W)
            check_button.grid(row=i + 1, column=1, padx=10, pady=10, sticky=tk.W)

        other_var = tk.IntVar()
        other_checkbox = tk.Checkbutton(symptom_window, text="Other", variable=other_var,
                                        command=lambda: unselect_other_symptoms(symptom_window))
        other_checkbox.grid(row=len(symptoms) + 1, columnspan=2, pady=10)

        submit_button = tk.Button(symptom_window, text="Submit",
                                  command=lambda: submit(symptoms_vars, other_var, symptom_window,
                                                         recommendation_window))
        submit_button.grid(row=len(symptoms) + 2, columnspan=2, pady=10)

    def unselect_other_symptoms(symptom_window):
        global symptoms_vars, other_var
        if other_var.get() == 1:
            for var in symptoms_vars:
                var.set(0)

    def submit(symptoms_vars, other_var, symptom_window, recommendation_window):
        selected_symptoms = [symptom_var.get() for symptom_var in symptoms_vars]
        recommendations = []

        if selected_symptoms[3] == 1 and selected_symptoms[0] == 1:
            recommendations.append(
                "For your pain and fever: take two 500mg paracetamol every 4 hours, 4 times a day.")
        elif selected_symptoms[3] == 1:
            recommendations.append("For your fever: take two 500mg paracetamol every 4 hours, 4 times a day.")
        elif selected_symptoms[0] == 1:
            recommendations.append("For pain: take two 500mg paracetamol every 4 hours, 4 times a day.")
        if selected_symptoms[1] == 1:
            recommendations.append("For inflammation: take a 200mg tablet of ibuprofen every 6 hours.")
        if selected_symptoms[2] == 1:
            recommendations.append("For your cough: take cough syrup and follow the instructions on the bottle.")
        if selected_symptoms[4] == 1:
            recommendations.append("For your allergic reaction: take a 10mg tablet of Cetirizine once a day.")
        if selected_symptoms[5] == 1:
            recommendations.append("For indigestion: take Gaviscon.")
        if selected_symptoms[6] == 1:
            recommendations.append("For itchy skin: Use hydrocortisone cream once a day.")
        if other_var.get() == 1:
            recommendations.append("Please consult a Doctor")

        if recommendations:
            display_recommendations(recommendations, symptom_window, recommendation_window)
        else:
            messagebox.showinfo("No Symptoms Selected", "No symptoms selected.")

    def display_recommendations(recommendations, symptom_window, local_recommendation_window):
        global recommendation_window
        recommendation_window = tk.Toplevel()
        recommendation_window.title("Medical Needs")
        recommendation_window.geometry("500x150")

        recommendations_label = tk.Label(recommendation_window, text="Recommendations:")
        recommendations_label.pack()

        recommended_medications = []

        for recommendation in recommendations:
            recommendation_text = tk.Label(recommendation_window, text="- " + recommendation)
            recommendation_text.pack()

            if "paracetamol" in recommendation.lower():
                recommended_medications.append(("Paracetamol", request_paracetamol))
            if "ibuprofen" in recommendation.lower():
                recommended_medications.append(("Ibuprofen", request_ibuprofen))
            if "cough syrup" in recommendation.lower():
                recommended_medications.append(("Cough Syrup", request_cough_syrup))
            if "cetirizine" in recommendation.lower():
                recommended_medications.append(("Cetirizine", request_cetirizine))
            if "gaviscon" in recommendation.lower():
                recommended_medications.append(("Gaviscon", request_gaviscon))
            if "hydrocortisone cream" in recommendation.lower():
                recommended_medications.append(("Hydrocortisone Cream", request_hydrocortisone_cream))

        if len(recommended_medications) > 1:
            request_medications_button = tk.Button(recommendation_window, text="Request All Medications",
                                                   command=lambda: request_medications(
                                                       [med[0] for med in recommended_medications]))
            request_medications_button.pack()
        else:
            for med_name, med_command in recommended_medications:
                button = tk.Button(recommendation_window, text=f"Request {med_name}", command=med_command)
                button.pack()

        if other_var.get() == 1:
            request_doctor_button = tk.Button(recommendation_window, text="Request a Doctor",
                                              command=request_doctor)
            request_doctor_button.pack()

    def request_medications(medications):
        global pain_relief_required, symptom_window, recommendation_window
        messagebox.showinfo("Request Medications", f"Medications requested: {', '.join(medications)}.")

        if "Paracetamol" in medications or "Ibuprofen" in medications:
            pR.set(True)
        if "Cetirizine" in medications:
            epi.set(True)
        if symptom_window:
            symptom_window.destroy()
        if recommendation_window:
            recommendation_window.destroy()

    def request_paracetamol():
        global symptom_window, recommendation_window
        messagebox.showinfo("Request Paracetamol", "Paracetamol requested.")
        pR.set(True)
        if symptom_window:
            symptom_window.destroy()
        if recommendation_window:
            recommendation_window.destroy()

    def request_ibuprofen():
        global symptom_window, recommendation_window
        messagebox.showinfo("Request Ibuprofen", "Ibuprofen requested.")
        pR.set(True)
        if symptom_window:
            symptom_window.destroy()
        if recommendation_window:
            recommendation_window.destroy()

    def request_cough_syrup():
        global symptom_window, recommendation_window
        messagebox.showinfo("Request Cough Syrup", "Cough Syrup requested.")
        if symptom_window:
            symptom_window.destroy()
        if recommendation_window:
            recommendation_window.destroy()

    def request_cetirizine():
        global symptom_window, recommendation_window
        messagebox.showinfo("Request Cetrizine", "Cetirizine requested.")
        epi.set(True)
        if symptom_window:
            symptom_window.destroy()
        if recommendation_window:
            recommendation_window.destroy()

    def request_gaviscon():
        global symptom_window, recommendation_window
        messagebox.showinfo("Request Gaviscon", "Gaviscon requested.")
        if symptom_window:
            symptom_window.destroy()
        if recommendation_window:
            recommendation_window.destroy()

    def request_hydrocortisone_cream():
        global symptom_window, recommendation_window
        messagebox.showinfo("Request Hydrocortisone Cream", "Hydrocortisone Cream requested.")
        if symptom_window:
            symptom_window.destroy()
        if recommendation_window:
            recommendation_window.destroy()

    def request_doctor():
        global symptom_window, recommendation_window
        messagebox.showinfo("Request a Doctor", "To request a doctor, please call your Admin on: 123456789.")
        if symptom_window:
            symptom_window.destroy()
        if recommendation_window:
            recommendation_window.destroy()
    
    def submit_form():
        name = nameEntry.get()
        surname = surnameEntry.get()
        campId = cIDDL.get()
        age = ageEntry.get()
        languages = lanEntry.get()
        gender = genDL.get()
        bloodType = BTDL.get()
        psyHealth = psyHDL.get()
        phyHealth = phyHDL.get()
        if fIDDL.get() == 'Generate new family ID':
            familyId = generate_new_family()
        else:
            familyId = fIDDL.get()
        (glutenFree, dairyFree, noNuts, veganInput, vegeInput, omnivore, none) = diet_options(dRDL.get())
        epipen = epi.get()
        painRelief = pR.get()
        bandagesInput = bandages.get()
        sanitaryProducts = sP.get()
        if (not name or not surname or not campId or not age or not languages or not gender or
                not bloodType or not psyHealth or not phyHealth or not familyId or
                epipen is None or painRelief is None or bandagesInput is None or
                sanitaryProducts is None):
            tk.messagebox.showwarning("Please fill in all blanks.", "Please fill in all blanks!")
        elif not alpha_check(name) or not alpha_check(surname) or not alpha_check(languages):
            tk.messagebox.showwarning("Invalid input", "Name, surname and languages are text-only")
        elif not age_check(age):
            tk.messagebox.showwarning("Age not valid!", "Age not valid!")
        elif camp_full(campId):
            tk.messagebox.showwarning("Camp at full capacity", "Current camp has met its capacity."
                                                               "\nPlease choose another camp")
        else:
            newRefugee = Refugee(name, surname, campId, age, languages, gender, bloodType, psyHealth, phyHealth,
                                 familyId, glutenFree, dairyFree, noNuts, veganInput, vegeInput, omnivore, epipen,
                                 painRelief, bandagesInput, sanitaryProducts)
            result = Refugee.create_refugee(newRefugee)
            if result:
                update_count_ref()
                tk.messagebox.showinfo("Success", "Refugee created")
            else:
                tk.messagebox.showinfo("Failed", "Failed to create refugee")

    submitBtn = tk.Button(create_menu, text="Create Refugee", command=submit_form)
    submitBtn.grid(row=30, column=1, columnspan=2)


def camp_full(campId):
    with setup_conn() as conn:
        cursor = conn.cursor()
        query = f"SELECT capacity, totalRefugees FROM camps WHERE campID = ?"
        cursor.execute(query, (campId,))
        result = cursor.fetchone()
        if result[0] > result[1]:
            return False
        else:
            return True

def view_refugee():
    global open_windows
    view_menu = tk.Tk()
    open_windows.append(view_menu)
    view_menu.title("View Refugee")
    view_menu.geometry("1000x500")

    columns = ('refugeeID', 'name', 'surname', 'campID', 'age', 'languages', 'gender', 'bloodType', 'psyHealth',
               'physHealth', 'familyID', 'glutenFree', 'dairyFree', 'noNuts', 'vegan', 'vegetarian',
               'omnivore', 'epipen', 'painRelief', 'bandages', 'sanitaryProducts')

    tree = ttk.Treeview(view_menu, columns=columns, show='headings')
    tree.heading('refugeeID', text='refugee ID')
    tree.heading('name', text='name')
    tree.heading('surname', text='surname')
    tree.heading('campID', text='camp ID')
    tree.heading('age', text='age')
    tree.heading('languages', text='languages')
    tree.heading('gender', text='gender')
    tree.heading('bloodType', text='blood type')
    tree.heading('psyHealth', text='mental health')
    tree.heading('physHealth', text='physical health')
    tree.heading('familyID', text='family ID')
    tree.heading('glutenFree', text='gluten free')
    tree.heading('dairyFree', text='dairy free')
    tree.heading('noNuts', text='no nuts')
    tree.heading('vegan', text='vegan')
    tree.heading('vegetarian', text='vegetarian')
    tree.heading('omnivore', text='omnivore')
    tree.heading('epipen', text='epipen')
    tree.heading('painRelief', text='pain relief')
    tree.heading('bandages', text='bandages')
    tree.heading('sanitaryProducts', text='sanitary products')

    tree.column('refugeeID', width=100)
    tree.column('name', width=100)
    tree.column('surname', width=100)
    tree.column('campID', width=50)
    tree.column('age', width=50)
    tree.column('languages', width=150)
    tree.column('gender', width=100)
    tree.column('bloodType', width=100)
    tree.column('psyHealth', width=100)
    tree.column('physHealth', width=100)
    tree.column('familyID', width=75)
    tree.column('glutenFree', width=75)
    tree.column('dairyFree', width=75)
    tree.column('noNuts', width=75)
    tree.column('vegan', width=75)
    tree.column('vegetarian', width=75)
    tree.column('omnivore', width=75)
    tree.column('epipen', width=75)
    tree.column('painRelief', width=75)
    tree.column('bandages', width=75)
    tree.column('sanitaryProducts', width=75)

    def bool_to_symbol(booL):
        if booL:
            return "Yes"
        else:
            return "No"

    result = Refugee.view_refugee()
    if result is not None:
        for row in result:
            newRef = Refugee(*row)
            tree.insert("", "end", values=(newRef.refugeeId, newRef.name, newRef.surname, newRef.campId, newRef.age,
                                           newRef.languages, newRef.gender, newRef.bloodType, newRef.psyHealth,
                                           newRef.physHealth, newRef.familyID, bool_to_symbol(newRef.glutenFree),
                                           bool_to_symbol(newRef.dairyFree), bool_to_symbol(newRef.noNuts),
                                           bool_to_symbol(newRef.vegan), bool_to_symbol(newRef.vegetarian),
                                           bool_to_symbol(newRef.omnivore), bool_to_symbol(newRef.epipen),
                                           bool_to_symbol(newRef.painRelief), bool_to_symbol(newRef.bandages),
                                           bool_to_symbol(newRef.sanitaryProducts)))

            tree.pack(expand=True, fill="both")
        tableExp = tk.Label(view_menu, text="This table consists of the details of all the members registered in the system.")
        tableExp.pack(side="bottom", pady=10)
    else:
        tk.messagebox.showinfo("No refugees", "No refugees")


def bool_to_symbol(booL):
    if booL:
        return "Yes"
    else:
        return "No"


def view_search_refugee(result):
    global open_windows
    view_menu = tk.Tk()
    open_windows.append(view_menu)
    view_menu.title("View Refugee")
    view_menu.geometry("1200x200")

    columns = ('refugeeID', 'name', 'surname', 'campID', 'age', 'languages', 'gender', 'bloodType', 'psyHealth',
               'physHealth', 'familyID', 'glutenFree', 'dairyFree', 'noNuts', 'vegan', 'vegetarian',
               'omnivore', 'epipen', 'painRelief', 'bandages', 'sanitaryProducts')

    tree = ttk.Treeview(view_menu, columns=columns, show='headings')
    tree.heading('refugeeID', text='refugee ID')
    tree.heading('name', text='name')
    tree.heading('surname', text='surname')
    tree.heading('campID', text='camp ID')
    tree.heading('age', text='age')
    tree.heading('languages', text='languages')
    tree.heading('gender', text='gender')
    tree.heading('bloodType', text='blood type')
    tree.heading('psyHealth', text='mental health')
    tree.heading('physHealth', text='physical health')
    tree.heading('familyID', text='family ID')
    tree.heading('glutenFree', text='gluten free')
    tree.heading('dairyFree', text='dairy free')
    tree.heading('noNuts', text='no nuts')
    tree.heading('vegan', text='vegan')
    tree.heading('vegetarian', text='vegetarian')
    tree.heading('omnivore', text='omnivore')
    tree.heading('epipen', text='epipen')
    tree.heading('painRelief', text='pain relief')
    tree.heading('bandages', text='bandages')
    tree.heading('sanitaryProducts', text='sanitary products')

    tree.column('refugeeID', width=100)
    tree.column('name', width=100)
    tree.column('surname', width=100)
    tree.column('campID', width=50)
    tree.column('age', width=50)
    tree.column('languages', width=150)
    tree.column('gender', width=100)
    tree.column('bloodType', width=100)
    tree.column('psyHealth', width=100)
    tree.column('physHealth', width=100)
    tree.column('familyID', width=75)
    tree.column('glutenFree', width=75)
    tree.column('dairyFree', width=75)
    tree.column('noNuts', width=75)
    tree.column('vegan', width=75)
    tree.column('vegetarian', width=75)
    tree.column('omnivore', width=75)
    tree.column('epipen', width=75)
    tree.column('painRelief', width=75)
    tree.column('bandages', width=75)
    tree.column('bandages', width=75)
    tree.column('sanitaryProducts', width=75)

    for row in result:
        newRef = Refugee(*row)
        tree.insert("", "end", values=(newRef.refugeeId, newRef.name, newRef.surname, newRef.campId, newRef.age,
                                       newRef.languages, newRef.gender, newRef.bloodType, newRef.psyHealth,
                                       newRef.physHealth, newRef.familyID, bool_to_symbol(newRef.glutenFree),
                                       bool_to_symbol(newRef.dairyFree), bool_to_symbol(newRef.noNuts),
                                       bool_to_symbol(newRef.vegan), bool_to_symbol(newRef.vegetarian),
                                       bool_to_symbol(newRef.omnivore), bool_to_symbol(newRef.epipen),
                                       bool_to_symbol(newRef.painRelief), bool_to_symbol(newRef.bandages),
                                       bool_to_symbol(newRef.sanitaryProducts)))

        tree.pack(expand=True, fill="both")
    tableExp = tk.Label(view_menu,
                        text="This table consists of the details of the searched refugee.")
    tableExp.pack(side="bottom", pady=10)



def search_refugee():
    global open_windows
    search_menu = tk.Toplevel()
    open_windows.append(search_menu)
    search_menu.title("Search Refugee")
    search_menu.geometry("500x200")

    mode = tk.StringVar(value="mode")

    def search_by_mode():
        for widget in search_menu.winfo_children():
            if isinstance(widget, (tk.Label, tk.Entry, tk.Button)):
                widget.destroy()

        if mode.get() == "name":
            nameLabel = tk.Label(search_menu, text="Name: ")
            nameLabel.pack()
            nameEntry = tk.Entry(search_menu)
            nameEntry.pack()

            surnameLabel = tk.Label(search_menu, text="Surname: ")
            surnameLabel.pack()
            surnameEntry = tk.Entry(search_menu)
            surnameEntry.pack()

            def search_by_name():
                name = nameEntry.get()
                surname = surnameEntry.get()
                with setup_conn() as connRef:
                    cursor = connRef.cursor()
                    cursor.execute("SELECT name, surname, campID, age, languages, gender, bloodType, psyHealth, "
                                   "physHealth, familyID, glutenFree, dairyFree, noNuts, vegan, vegetarian, "
                                   "omnivore, epipen, painRelief, bandages, sanitaryProducts, refugeeID"
                                   " FROM refugee WHERE name = ? AND surname = ?", (name, surname))
                    result = cursor.fetchall()
                    if len(result) != 0:
                        view_search_refugee(result)
                    else:
                        tk.messagebox.showwarning("Refugee not found", "Refugee not found")

            submitBtn = tk.Button(search_menu, text="Search Refugee", command=search_by_name)
            submitBtn.pack()

        elif mode.get() == "id":
            iDLabel = tk.Label(search_menu, text="Refugee ID: ")
            iDLabel.pack()
            iDEntry = tk.Entry(search_menu)
            iDEntry.pack()

            def search_by_id():
                refID = iDEntry.get()
                if not refID.isdigit():
                        tk.messagebox.showerror("Invalid Input", "Please enter a valid numeric ID.")
                else:
                    with setup_conn() as connRef:
                        cursor = connRef.cursor()
                        cursor.execute("SELECT name, surname, campID, age, languages, gender, bloodType, psyHealth, "
                                    "physHealth, familyID, glutenFree, dairyFree, noNuts, vegan, vegetarian, "
                                    "omnivore, epipen, painRelief, bandages, sanitaryProducts, refugeeID"
                                    " FROM refugee WHERE refugeeID = ?", (refID,))
                        result = cursor.fetchall()
                        if len(result) != 0:
                            view_search_refugee(result)
                        else:
                            tk.messagebox.showwarning("Refugee not found", "Refugee not found")

            submitBtn = tk.Button(search_menu, text="Search Refugee", command=search_by_id)
            submitBtn.pack()

    tk.Radiobutton(search_menu, text="search by name", variable=mode, value="name", command=search_by_mode).pack()
    tk.Radiobutton(search_menu, text="search by id", variable=mode, value="id", command=search_by_mode).pack()

    search_by_mode()


def yn_to_bool(value):
    if value == 'No':
        return False
    if value == 'Yes':
        return True


def num_to_yn(value):
    if value == 0:
        return 'No'
    if value == 1:
        return 'Yes'


def num_to_bool(value):
    if value == 0:
        return False
    if value == 1:
        return True


def edit_refugee():
    global open_windows
    edit_menu = tk.Tk()
    open_windows.append(edit_menu)
    edit_menu.title("Edit Refugee")
    edit_menu.geometry("750x200")

    iDLabel = tk.Label(edit_menu, text="Enter Refugee ID to edit information: ")
    iDLabel.grid(row=0, column=0)
    iDEntry = tk.Entry(edit_menu)
    iDEntry.grid(row=0, column=1)

    def edit_refugee_backend():
        refID = iDEntry.get()
        newRef = None
        if not refID:
            pass
        elif not numeric_check(refID):
            pass
        else:
            with setup_conn() as connRef:
                cursor = connRef.cursor()
                cursor.execute("SELECT name, surname, campID, age, languages, gender, bloodType, psyHealth, "
                               "physHealth, familyID, glutenFree, dairyFree, noNuts, vegan, vegetarian, "
                               "omnivore, epipen, painRelief, bandages, sanitaryProducts, refugeeID"
                               " FROM refugee WHERE refugeeID = ?", (refID,))
                result = cursor.fetchall()
                if result is not None:
                    for row in result:
                        newRef = Refugee(*row)
                else:
                    tk.messagebox.showinfo(title="Error", message="Refugee not exist")
        if newRef is None:
            tk.messagebox.showinfo(title="Error", message="Please enter a valid refugee ID")
        else:

            editRefID = newRef.refugeeId

            edit_info_menu = tk.Tk()
            edit_info_menu.title("Edit Refugee Information")
            edit_info_menu.geometry("1000x500")

            nameLabel = tk.Label(edit_info_menu, text="Refugee name: ")
            nameLabel.grid(row=0, column=0)
            nameEntry = tk.Entry(edit_info_menu)
            nameEntry.grid(row=0, column=1)
            nameEntry.insert(0, newRef.name)

            surnameLabel = tk.Label(edit_info_menu, text="Refugee surname: ")
            surnameLabel.grid(row=0, column=2)
            surnameEntry = tk.Entry(edit_info_menu)
            surnameEntry.grid(row=0, column=3)
            surnameEntry.insert(0, newRef.surname)

            cIDOptions = get_camp()
            cIDLabel = tk.Label(edit_info_menu, text="Refugee camp ID: ")
            cIDLabel.grid(row=1, column=0)
            cIDDL = ttk.Combobox(edit_info_menu, values=cIDOptions, state="readonly")
            cIDDL.grid(row=1, column=1)
            cIDDL.set(newRef.campId)

            ageLabel = tk.Label(edit_info_menu, text="Refugee age: ")
            ageLabel.grid(row=1, column=2)
            ageEntry = tk.Entry(edit_info_menu)
            ageEntry.grid(row=1, column=3)
            ageEntry.insert(0, newRef.age)

            lanOptions = ["Chinese","Spanish","English","Hindi","Arabic","Bengali","Portuguese","Russian","Urdu","Other"]
            lanLabel = tk.Label(edit_info_menu, text="Refugee languages: ")
            lanLabel.grid(row=2, column=0)
            lanEntry = ttk.Combobox(edit_info_menu, values=lanOptions, state='readonly')
            lanEntry.grid(row=2, column=1)
            lanEntry.set(newRef.languages)

            genOptions = ['Male', 'Female', 'Others']
            genLabel = tk.Label(edit_info_menu, text="Refugee gender: ")
            genLabel.grid(row=2, column=2)
            genDL = ttk.Combobox(edit_info_menu, values=genOptions, state='readonly')
            genDL.grid(row=2, column=3)
            genDL.set(newRef.gender)

            BTOptions = ["A+", "A-", "AB+", "AB-", "B+", "B-", "O+", "O-"]
            BTLabel = tk.Label(edit_info_menu, text="Refugee blood type: ")
            BTLabel.grid(row=3, column=0)
            BTDL = ttk.Combobox(edit_info_menu, values=BTOptions, state='readonly')
            BTDL.grid(row=3, column=1)
            BTDL.set(newRef.bloodType)

            healthOptions = ['Excellent', 'Good', 'Moderate', 'Fair', 'Poor']
            psyHLabel = tk.Label(edit_info_menu, text="Refugee psychological health: ")
            psyHLabel.grid(row=3, column=2)
            psyHDL = ttk.Combobox(edit_info_menu, values=healthOptions, state='readonly')
            psyHDL.grid(row=3, column=3)
            psyHDL.set(newRef.psyHealth)

            phyHLabel = tk.Label(edit_info_menu, text="Refugee physical health: ")
            phyHLabel.grid(row=4, column=0)
            phyHDL = ttk.Combobox(edit_info_menu, values=healthOptions, state='readonly')
            phyHDL.grid(row=4, column=1)
            phyHDL.set(newRef.physHealth)

            familyList = get_family()
            fIDOptions = familyList
            fIDOptions.append('Generate new family ID')
            fIDLabel = tk.Label(edit_info_menu, text="Refugee family ID: ")
            fIDLabel.grid(row=4, column=2)
            fIDDL = ttk.Combobox(edit_info_menu, values=fIDOptions, state='readonly')
            fIDDL.grid(row=4, column=3)
            fIDDL.set(newRef.familyID)

            dietOptions = ['Gluten Free', 'Dairy Free', 'No Nuts', 'Vegan', 'Vegetarian', 'Omnivore', 'None']
            def display_dO(gF, dF, nN, vegan, vege, omni):
                if gF == 1:
                    return dietOptions[0]
                elif dF == 1:
                    return dietOptions[1]
                elif nN == 1:
                    return dietOptions[2]
                elif vegan == 1:
                    return dietOptions[3]
                elif vege == 1:
                    return dietOptions[4]
                elif omni == 1:
                    return dietOptions[5]
                else:
                    return dietOptions[6]

            dietLabel = tk.Label(edit_info_menu, text="Diet options: ")
            dietLabel.grid(row=5, column=1)
            dRDL = ttk.Combobox(edit_info_menu, values=dietOptions, state='readonly')
            dRDL.grid(row=5, column=2)
            dRDL.set(display_dO(newRef.glutenFree, newRef.dairyFree, newRef.noNuts, newRef.vegan, newRef.vegetarian,
                                newRef.omnivore))

            def diet_options(choice, gF=False, dF=False, nN=False, Vegan=False, Vege=False, Omnivore=False, none = False):
                match choice:
                    case 'Gluten Free':
                        gF = True
                    case 'Dairy Free':
                        dF = True
                    case 'No Nuts':
                        nN = True
                    case 'Vegan':
                        Vegan = True
                    case 'Vegetarian':
                        Vege = True
                    case 'Omnivore':
                        Omnivore = True
                return gF, dF, nN, Vegan, Vege, Omnivore, none

            medicalLabel = tk.Label(edit_info_menu, text="If you need the following resources please choose yes: ")
            medicalLabel.grid(row=6, column=1)

            options = ['Yes', 'No']
            epiLabel = tk.Label(edit_info_menu, text=f"Epipen: {num_to_yn(newRef.epipen)}")
            epiLabel.grid(row=11, column=0)
            epi = num_to_bool(newRef.epipen)
            epiDL = ttk.Combobox(edit_info_menu, values=options, state='readonly')
            epiDL.grid(row=11, column=1)
            epiDL.set('Yes' if epi else 'No')

            pRLabel = tk.Label(edit_info_menu, text=f"Plain relief: {num_to_yn(newRef.painRelief)}")
            pRLabel.grid(row=12, column=0)
            pR = num_to_bool(newRef.painRelief)
            pRDL = ttk.Combobox(edit_info_menu, values=options, state='readonly')
            pRDL.grid(row=12, column=1)
            pRDL.set('Yes' if pR else 'No')

            bLabel = tk.Label(edit_info_menu, text=f"Bandages: {num_to_yn(newRef.bandages)}")
            bLabel.grid(row=13, column=0)
            bandages = num_to_bool(newRef.bandages)
            bDL = ttk.Combobox(edit_info_menu, values=options, state='readonly')
            bDL.grid(row=13, column=1)
            bDL.set('Yes' if bandages else 'No')

            sPLabel = tk.Label(edit_info_menu, text=f"Sanitary products: {num_to_yn(newRef.sanitaryProducts)}")
            sPLabel.grid(row=14, column=0)
            sP = num_to_bool(newRef.sanitaryProducts)
            sPDL = ttk.Combobox(edit_info_menu, values=options, state='readonly')
            sPDL.grid(row=14, column=1)
            sPDL.set('Yes' if sP else 'No')

            def submit_form():
                name = nameEntry.get()
                surname = surnameEntry.get()
                campId = cIDDL.get()
                age = ageEntry.get()
                languages = lanEntry.get()
                gender = genDL.get()
                bloodType = BTDL.get()
                psyHealth = psyHDL.get()
                phyHealth = phyHDL.get()
                if fIDDL.get() == 'Generate new family ID':
                    familyId = generate_new_family()
                else:
                    familyId = fIDDL.get()
                (glutenFree, dairyFree, noNuts, veganInput, vegeInput, omnivore, none) = diet_options(dRDL.get())
                epipen = yn_to_bool(epiDL.get())
                painRelief = yn_to_bool(pRDL.get())
                bandagesInput = yn_to_bool(bDL.get())
                sanitaryProducts = yn_to_bool(sPDL.get())
                if not name or not surname or not campId or not age or not languages or not gender:
                    tk.messagebox.showwarning("Please fill in all blanks.", "Please fill in all blanks!")
                elif not alpha_check(name) or not alpha_check(surname) or not alpha_check(languages):
                    tk.messagebox.showwarning("Invalid input", "Name, surname and languages are text-only")
                elif not age_check(age):
                    tk.messagebox.showwarning("Age not valid!", "Age not valid!")
                elif camp_full(campId):
                    tk.messagebox.showwarning("Camp at full capacity", "Current camp has met its capacity."
                                                                       "\nPlease choose another camp")
                else:
                    newRefugee = Refugee(name, surname, campId, age, languages, gender, bloodType, psyHealth, phyHealth,
                                         familyId, glutenFree, dairyFree, noNuts, veganInput, vegeInput, omnivore, epipen,
                                         painRelief, bandagesInput, sanitaryProducts)
                    with setup_conn() as connRefE:
                        cursorE = connRefE.cursor()
                        sql = """
                                        UPDATE refugee 
                                        SET name = ?, surname = ?, campId = ?, age = ?, languages = ?, gender = ?, 
                                        bloodType = ?, psyHealth = ?, physHealth = ?, familyID = ?, 
                                        glutenFree = ?, dairyFree = ?, noNuts = ?, vegan = ?, vegetarian = ?, 
                                        omnivore = ?, epipen = ?, painRelief = ?, bandages = ?, sanitaryProducts = ?
                                        WHERE refugeeId = ?
                                        """
                        cursorE.execute(sql, (newRefugee.name, newRefugee.surname, newRefugee.campId,
                                              newRefugee.age, newRefugee.languages, newRefugee.gender,
                                              newRefugee.bloodType, newRefugee.psyHealth, newRefugee.physHealth,
                                              newRefugee.familyID, newRefugee.glutenFree, newRefugee.dairyFree,
                                              newRefugee.noNuts, newRefugee.vegan, newRefugee.vegetarian,
                                              newRefugee.omnivore, newRefugee.epipen, newRefugee.painRelief,
                                              newRefugee.bandages, newRefugee.sanitaryProducts,
                                              editRefID))
                        connRefE.commit()
                    if cursorE.rowcount > 0:
                        update_count_ref()
                        tk.messagebox.showinfo("Success", "Refugee information updated")
                    else:
                        tk.messagebox.showinfo("Failed", "Failed to update refugee information")

            submitBtnE = tk.Button(edit_info_menu, text="Update Refugee Information", command=submit_form)
            submitBtnE.grid(row=15, column=0, columnspan=2)

    submitBtn = tk.Button(edit_menu, text="Search and Edit", command=edit_refugee_backend)
    submitBtn.grid(row=0, column=2)


def view_by_family():
    global open_windows
    view_family_menu = tk.Tk()
    open_windows.append(view_family_menu)
    view_family_menu.title("Family")
    view_family_menu.geometry("800x800")

    familyList = get_family()
    famIDInt = [int(familyID) for familyID in familyList]
    columns = (
        'familyID', 'refugeeID', 'name', 'surname', 'campID', 'age', 'languages', 'gender', 'bloodType', 'psyHealth',
        'physHealth', 'glutenFree', 'dairyFree', 'noNuts', 'vegan', 'vegetarian',
        'omnivore', 'epipen', 'painRelief', 'bandages', 'sanitaryProducts')

    tree = ttk.Treeview(view_family_menu, columns=columns, show='headings')

    for family in famIDInt:
        tree.heading('refugeeID', text='refugee ID')
        tree.heading('name', text='name')
        tree.heading('surname', text='surname')
        tree.heading('campID', text='camp ID')
        tree.heading('age', text='age')
        tree.heading('languages', text='languages')
        tree.heading('gender', text='gender')
        tree.heading('bloodType', text='blood type')
        tree.heading('psyHealth', text='mental health')
        tree.heading('physHealth', text='physical health')
        tree.heading('familyID', text='family ID')
        tree.heading('glutenFree', text='gluten free')
        tree.heading('dairyFree', text='dairy free')
        tree.heading('noNuts', text='no nuts')
        tree.heading('vegan', text='vegan')
        tree.heading('vegetarian', text='vegetarian')
        tree.heading('omnivore', text='omnivore')
        tree.heading('epipen', text='epipen')
        tree.heading('painRelief', text='pain relief')
        tree.heading('bandages', text='bandages')
        tree.heading('sanitaryProducts', text='sanitary products')

        tree.column('refugeeID', width=100)
        tree.column('name', width=100)
        tree.column('surname', width=100)
        tree.column('campID', width=50)
        tree.column('age', width=50)
        tree.column('languages', width=150)
        tree.column('gender', width=100)
        tree.column('bloodType', width=100)
        tree.column('psyHealth', width=100)
        tree.column('physHealth', width=100)
        tree.column('familyID', width=75)
        tree.column('glutenFree', width=75)
        tree.column('dairyFree', width=75)
        tree.column('noNuts', width=75)
        tree.column('vegan', width=75)
        tree.column('vegetarian', width=75)
        tree.column('omnivore', width=75)
        tree.column('epipen', width=75)
        tree.column('painRelief', width=75)
        tree.column('bandages', width=75)
        tree.column('sanitaryProducts', width=75)
        with setup_conn() as connRef:
            cursor = connRef.cursor()
            cursor.execute("SELECT name, surname, campID, age, languages, gender, bloodType, psyHealth, "
                           "physHealth, familyID, glutenFree, dairyFree, noNuts, vegan, vegetarian, "
                           "omnivore, epipen, painRelief, bandages, sanitaryProducts, refugeeID "
                           "FROM refugee WHERE familyID = ?", (family,))
            result = cursor.fetchall()
            if len(result) > 1:
                for row in result:
                    newRef = Refugee(*row)
                    tree.insert("", "end",
                                values=(newRef.familyID, newRef.refugeeId, newRef.name, newRef.surname, newRef.campId,
                                        newRef.age, newRef.languages, newRef.gender, newRef.bloodType, newRef.psyHealth,
                                        newRef.physHealth, bool_to_symbol(newRef.glutenFree),
                                        bool_to_symbol(newRef.dairyFree), bool_to_symbol(newRef.noNuts),
                                        bool_to_symbol(newRef.vegan), bool_to_symbol(newRef.vegetarian),
                                        bool_to_symbol(newRef.omnivore), bool_to_symbol(newRef.epipen),
                                        bool_to_symbol(newRef.painRelief), bool_to_symbol(newRef.bandages),
                                        bool_to_symbol(newRef.sanitaryProducts)))
                empty_row = ('',) * len(columns)
                tree.insert("", "end", values=empty_row)
            tree.pack(expand=True, fill="both")

    tableExp = tk.Label(view_family_menu, text="This table consists of the details of "
                                               "all the members in families that has more than one member registered.")
    tableExp.pack(side="bottom", pady=10)




def search_family_menu():
    global open_windows
    search_family_menu = tk.Tk()
    open_windows.append(search_family_menu)
    search_family_menu.title("Search Family")
    search_family_menu.geometry("500x200")

    famIDLabel = tk.Label(search_family_menu, text="Enter Family ID: ")
    famIDLabel.grid(row=0, column=0)
    famIDEntry = tk.Entry(search_family_menu)
    famIDEntry.grid(row=0, column=1)

    def search_family():
        famID = famIDEntry.get()

        with setup_conn() as connRef:
            cursor = connRef.cursor()
            cursor.execute("SELECT name, surname, campID, age, languages, gender, bloodType, psyHealth, "
                           "physHealth, familyID, glutenFree, dairyFree, noNuts, vegan, vegetarian, "
                           "omnivore, epipen, painRelief, bandages, sanitaryProducts, refugeeID "
                           "FROM refugee WHERE familyID = ?", (famID,))

            result = cursor.fetchall()
            if len(result) > 1:
                view_searched_family = tk.Tk()
                view_searched_family.title("Search Result")
                view_searched_family.geometry("1200x500")
                columns = (
                    'familyID', 'refugeeID', 'name', 'surname', 'campID', 'age', 'languages', 'gender', 'bloodType',
                    'psyHealth',
                    'physHealth', 'glutenFree', 'dairyFree', 'noNuts', 'vegan', 'vegetarian',
                    'omnivore', 'epipen', 'painRelief', 'bandages', 'sanitaryProducts')

                tree = ttk.Treeview(view_searched_family, columns=columns, show='headings')
                tree.heading('refugeeID', text='refugee ID')
                tree.heading('name', text='name')
                tree.heading('surname', text='surname')
                tree.heading('campID', text='camp ID')
                tree.heading('age', text='age')
                tree.heading('languages', text='languages')
                tree.heading('gender', text='gender')
                tree.heading('bloodType', text='blood type')
                tree.heading('psyHealth', text='mental health')
                tree.heading('physHealth', text='physical health')
                tree.heading('familyID', text='family ID')
                tree.heading('glutenFree', text='gluten free')
                tree.heading('dairyFree', text='dairy free')
                tree.heading('noNuts', text='no nuts')
                tree.heading('vegan', text='vegan')
                tree.heading('vegetarian', text='vegetarian')
                tree.heading('omnivore', text='omnivore')
                tree.heading('epipen', text='epipen')
                tree.heading('painRelief', text='pain relief')
                tree.heading('bandages', text='bandages')
                tree.heading('sanitaryProducts', text='sanitary products')

                tree.column('refugeeID', width=100)
                tree.column('name', width=100)
                tree.column('surname', width=100)
                tree.column('campID', width=50)
                tree.column('age', width=50)
                tree.column('languages', width=150)
                tree.column('gender', width=100)
                tree.column('bloodType', width=100)
                tree.column('psyHealth', width=100)
                tree.column('physHealth', width=100)
                tree.column('familyID', width=75)
                tree.column('glutenFree', width=75)
                tree.column('dairyFree', width=75)
                tree.column('noNuts', width=75)
                tree.column('vegan', width=75)
                tree.column('vegetarian', width=75)
                tree.column('omnivore', width=75)
                tree.column('epipen', width=75)
                tree.column('painRelief', width=75)
                tree.column('bandages', width=75)
                tree.column('sanitaryProducts', width=75)

                for row in result:
                    newRef = Refugee(*row)
                    tree.insert("", "end",
                                values=(newRef.familyID, newRef.refugeeId, newRef.name, newRef.surname, newRef.campId,
                                        newRef.age, newRef.languages, newRef.gender, newRef.bloodType, newRef.psyHealth,
                                        newRef.physHealth, bool_to_symbol(newRef.glutenFree),
                                        bool_to_symbol(newRef.dairyFree), bool_to_symbol(newRef.noNuts),
                                        bool_to_symbol(newRef.vegan), bool_to_symbol(newRef.vegetarian),
                                        bool_to_symbol(newRef.omnivore), bool_to_symbol(newRef.epipen),
                                        bool_to_symbol(newRef.painRelief), bool_to_symbol(newRef.bandages),
                                        bool_to_symbol(newRef.sanitaryProducts)))
                    tree.pack(expand=True, fill="both")
                tableExp = tk.Label(search_family_menu, text="This table consists of the details of all the members "
                                                             "in the searched family.")
                tableExp.pack(side="bottom", pady=10)
            else:
                tk.messagebox.showwarning("Family not found", "Family not found")

    submitBtn = tk.Button(search_family_menu, text="Search Family", command=search_family)
    submitBtn.grid(row=1, column=0, columnspan=2)


# def medic_attention():
#     medic_attention = tk.Toplevel()
#     medic_attention.title("Refugees Needing Medical Attention")
#     medic_attention.geometry("500x200")

#     with setup_conn() as connRef:
#         cursor = connRef.cursor()
#         cursor.execute("SELECT refugeeID, name, surname, campID, age, languages, gender, bloodType, psyHealth, physHealth FROM refugee WHERE psyHealth IN ('Moderate', 'Fair', 'Poor')")    
#         low_psy_Health_data = cursor.fetchall()
        
#     with setup_conn() as connRef:
#         cursor = connRef.cursor()
#         cursor.execute("SELECT refugeeID, name, surname, campID, age, languages, gender, bloodType, psyHealth, physHealth FROM refugee WHERE physHealth IN ('Moderate', 'Fair', 'Poor')")
#         low_phys_Health_data = cursor.fetchall()    

#     if len(low_psy_Health_data) > 1:
#         view_low_psy_Health = tk.Toplevel()
#         view_low_psy_Health.title("Low Psycological Health Result")
#         view_low_psy_Health.geometry("1200x500")
#         columns = ('refugeeID', 'name', 'surname', 'campID', 'age', 'languages', 'gender', 'bloodType', 'psyHealth', 'physHealth')
#         tree = ttk.Treeview(view_low_psy_Health, columns=columns, show='headings')

#         tree.heading('refugeeID', text='refugee ID')
#         tree.heading('name', text='name')
#         tree.heading('surname', text='surname')
#         tree.heading('campID', text='camp ID')
#         tree.heading('age', text='age')
#         tree.heading('languages', text='languages')
#         tree.heading('gender', text='gender')
#         tree.heading('bloodType', text='blood type')
#         tree.heading('psyHealth', text='mental health')
#         tree.heading('physHealth', text='physical health')

#         tree.column('refugeeID', width=100)
#         tree.column('name', width=100)
#         tree.column('surname', width=100)
#         tree.column('campID', width=50)
#         tree.column('age', width=50)
#         tree.column('languages', width=150)
#         tree.column('gender', width=100)
#         tree.column('bloodType', width=100)
#         tree.column('psyHealth', width=100)
#         tree.column('physHealth', width=100)

#     if len(low_phys_Health_data) > 1:
#         view_low_phys_Health = tk.Toplevel()
#         view_low_phys_Health.title("Low Physical Health Result")
#         view_low_phys_Health.geometry("1200x500")
#         columns = ('refugeeID', 'name', 'surname', 'campID', 'age', 'languages', 'gender', 'bloodType', 'psyHealth', 'physHealth')
#         tree = ttk.Treeview(view_low_phys_Health, columns=columns, show='headings')



def medic_attention():
    with setup_conn() as connRef:
        cursor = connRef.cursor()

        # Fetch low psychological health results
        cursor.execute("SELECT refugeeID, name, surname, campID, age, languages, gender, bloodType, psyHealth, physHealth FROM refugee WHERE psyHealth IN ('Moderate', 'Fair', 'Poor')")
        low_psy_health_data = cursor.fetchall()

        # Fetch low physiological health results
        cursor.execute("SELECT refugeeID, name, surname, campID, age, languages, gender, bloodType, psyHealth, physHealth FROM refugee WHERE physHealth IN ('Moderate', 'Fair', 'Poor')")
        low_phys_health_data = cursor.fetchall()

    # Create the main window
    global open_windows
    medic_attention = tk.Tk()
    open_windows.append(medic_attention)
    medic_attention.title("Refugees Needing Medical Attention")
    medic_attention.geometry("1200x800")

    # Display all refugees
    columns = ('refugeeID', 'name', 'surname', 'campID', 'age', 'languages', 'gender', 'bloodType', 'psyHealth', 'physHealth')
    tree = ttk.Treeview(medic_attention, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    if low_psy_health_data:
        frame_low_psy_health = ttk.Frame(medic_attention)
        frame_low_psy_health.pack(pady=10)

        label_low_psy_health = ttk.Label(frame_low_psy_health, text="Low Psychological Health Results")
        label_low_psy_health.pack()

        tree_low_psy_health = ttk.Treeview(frame_low_psy_health, columns=columns, show='headings')

        for col in columns:
            tree_low_psy_health.heading(col, text=col)
            tree_low_psy_health.column(col, width=100)

        for row in low_psy_health_data:
            tree_low_psy_health.insert('', 'end', values=row)

        tree_low_psy_health.pack(padx=10, pady=10)
        tableExp = tk.Label(frame_low_psy_health,
                            text="This table consists of all the members with mental health lower than \'Good\'.")
        tableExp.pack(side="bottom", pady=10)

    if low_phys_health_data:
        frame_low_phys_health = ttk.Frame(medic_attention)
        frame_low_phys_health.pack(pady=10)

        label_low_phys_health = ttk.Label(frame_low_phys_health, text="Low Physiological Health Results")
        label_low_phys_health.pack()

        tree_low_phys_health = ttk.Treeview(frame_low_phys_health, columns=columns, show='headings')

        for col in columns:
            tree_low_phys_health.heading(col, text=col)
            tree_low_phys_health.column(col, width=100)

        for row in low_phys_health_data:
            tree_low_phys_health.insert('', 'end', values=row)

        tree_low_phys_health.pack(padx=10, pady=10)
        tableExp = tk.Label(frame_low_phys_health,
                            text="This table consists of all the members with physical health lower than \'Good\'.")
        tableExp.pack(side="bottom", pady=10)

    medic_attention.mainloop()

def request_otc_med():
    symptoms_page()

symptoms = ["Pain", "Inflammation", "Cough", "Fever", "Allergic Reaction", "Indigestion", "Itchy Skin"]
symptoms_vars = []
symptom_window = None
recommendation_window = None

def symptoms_page():
    global symptoms_vars, other_var, symptom_window
    symptoms_vars = [tk.IntVar() for _ in symptoms]

    symptom_window = tk.Toplevel()
    symptom_window.title("Symptom Table")
    symptom_window.geometry("800x400")

    familyList = get_family()
    fIDOptions = familyList
    fIDLabel = tk.Label(symptom_window, text="Refugee family ID: ")
    fIDLabel.grid(row=0, column=0, padx=10, pady=10)
    fIDDL = ttk.Combobox(symptom_window, values=get_family(), state='readonly')
    fIDDL.grid(row=0, column=1, padx=10, pady=10)

    cIDOptions = get_camp()
    cIDLabel = tk.Label(symptom_window, text="Refugee camp ID: ")
    cIDLabel.grid(row=0, column=2, padx=10, pady=10)
    cIDDL = ttk.Combobox(symptom_window, values=get_camp(), state="readonly")
    cIDDL.grid(row=0, column=3, padx=10, pady=10)

    message_label = tk.Label(symptom_window,
                             text="Please check the box if they only have these symptoms otherwise, click 'Other'.")
    message_label.grid(row=1, column=0, columnspan=4, pady=20)

    for i, symptom in enumerate(symptoms):
        row = 2 + i // 2
        col = (i % 2) * 2
        label = tk.Label(symptom_window, text=symptom)
        label.grid(row=row, column=col, padx=10, pady=10, sticky=tk.W)
        check_button = tk.Checkbutton(symptom_window, variable=symptoms_vars[i])
        check_button.grid(row=row, column=col + 1, padx=10, pady=10, sticky=tk.W)

    other_var = tk.IntVar()
    other_row = 2 + (len(symptoms) + 1) // 2
    other_checkbox = tk.Checkbutton(symptom_window, text="Other", variable=other_var,
                                    command=lambda: unselect_other_symptoms(symptom_window))
    other_checkbox.grid(row=other_row, column=0, columnspan=2, pady=10)

    submit_button = tk.Button(symptom_window, text="Submit",
                              command=lambda: submit(symptoms_vars, other_var, symptom_window, recommendation_window))
    submit_button.grid(row=other_row, column=2, columnspan=2, pady=10)


def unselect_other_symptoms(symptom_window):
    global symptoms_vars, other_var
    if other_var.get() == 1:
        for var in symptoms_vars:
            var.set(0)


def submit(symptoms_vars, other_var, symptom_window, recommendation_window):
    selected_symptoms = [symptom_var.get() for symptom_var in symptoms_vars]
    recommendations = []

    if selected_symptoms[3] == 1 and selected_symptoms[0] == 1:
        recommendations.append(
            "For your pain and fever: take two 500mg paracetamol every 4 hours, 4 times a day.")
    elif selected_symptoms[3] == 1:
        recommendations.append("For your fever: take two 500mg paracetamol every 4 hours, 4 times a day.")
    elif selected_symptoms[0] == 1:
        recommendations.append("For pain: take two 500mg paracetamol every 4 hours, 4 times a day.")
    if selected_symptoms[1] == 1:
        recommendations.append("For inflammation: take a 200mg tablet of ibuprofen every 6 hours.")
    if selected_symptoms[2] == 1:
        recommendations.append("For your cough: take cough syrup and follow the instructions on the bottle.")
    if selected_symptoms[4] == 1:
        recommendations.append("For your allergic reaction: take a 10mg tablet of Cetirizine once a day.")
    if selected_symptoms[5] == 1:
        recommendations.append("For indigestion: take Gaviscon.")
    if selected_symptoms[6] == 1:
        recommendations.append("For itchy skin: Use hydrocortisone cream once a day.")
    if other_var.get() == 1:
        recommendations.append("Please consult a Doctor")

    if recommendations:
        display_recommendations(recommendations, symptom_window, recommendation_window)
    else:
        messagebox.showinfo("No Symptoms Selected", "No symptoms selected.")

def display_recommendations(recommendations, symptom_window, local_recommendation_window):
    global recommendation_window
    recommendation_window = tk.Toplevel()
    recommendation_window.title("Medical Needs")
    recommendation_window.geometry("500x150")

    recommendations_label = tk.Label(recommendation_window, text="Recommendations:")
    recommendations_label.pack()

    recommended_medications = []

    for recommendation in recommendations:
        recommendation_text = tk.Label(recommendation_window, text="- " + recommendation)
        recommendation_text.pack()

        if "paracetamol" in recommendation.lower():
            recommended_medications.append(("Paracetamol", request_paracetamol))
        if "ibuprofen" in recommendation.lower():
            recommended_medications.append(("Ibuprofen", request_ibuprofen))
        if "cough syrup" in recommendation.lower():
            recommended_medications.append(("Cough Syrup", request_cough_syrup))
        if "cetirizine" in recommendation.lower():
            recommended_medications.append(("Cetirizine", request_cetirizine))
        if "gaviscon" in recommendation.lower():
            recommended_medications.append(("Gaviscon", request_gaviscon))
        if "hydrocortisone cream" in recommendation.lower():
            recommended_medications.append(("Hydrocortisone Cream", request_hydrocortisone_cream))

    if len(recommended_medications) > 1:
        request_medications_button = tk.Button(recommendation_window, text="Request All Medications",
                                                command=lambda: request_medications(
                                                    [med[0] for med in recommended_medications]))
        request_medications_button.pack()
    else:
        for med_name, med_command in recommended_medications:
            button = tk.Button(recommendation_window, text=f"Request {med_name}", command=med_command)
            button.pack()

    if other_var.get() == 1:
        request_doctor_button = tk.Button(recommendation_window, text="Request a Doctor",
                                            command=request_doctor)
        request_doctor_button.pack()

def request_medications(medications):
    global pain_relief_required, symptom_window, recommendation_window
    messagebox.showinfo("Request Medications", f"To obtain: {', '.join(medications)}, please contact your admin to book a doctor on: \n"
                                               f"123456789")

    if "Paracetamol" in medications or "Ibuprofen" in medications:
        pass
    if "Cetirizine" in medications:
        pass
    if symptom_window:
        symptom_window.destroy()
    if recommendation_window:
        recommendation_window.destroy()

def request_paracetamol():
    global symptom_window, recommendation_window
    messagebox.showinfo("Request Paracetamol", "Paracetamol can be requested by contacting your admin to request a Doctor on : \n"
                                               "123456789")
    if symptom_window:
        symptom_window.destroy()
    if recommendation_window:
        recommendation_window.destroy()

def request_ibuprofen():
    global symptom_window, recommendation_window
    messagebox.showinfo("Request Ibuprofen", "Ibuprofen can be requested by contacting your admin to request a Doctor on : \n"
                                               "123456789")
    if symptom_window:
        symptom_window.destroy()
    if recommendation_window:
        recommendation_window.destroy()

def request_cough_syrup():
    global symptom_window, recommendation_window
    messagebox.showinfo("Request Cough Syrup", "Cough Syrup can be requested by contacting your admin to request a Doctor on : \n"
                                               "123456789")
    if symptom_window:
        symptom_window.destroy()
    if recommendation_window:
        recommendation_window.destroy()

def request_cetirizine():
    global symptom_window, recommendation_window
    messagebox.showinfo("Request Cetrizine", "Cetirizine can be obtained by contacting your admin to request a Doctor on : \n"
                                               "123456789")
    if symptom_window:
        symptom_window.destroy()
    if recommendation_window:
        recommendation_window.destroy()


def request_gaviscon():
    global symptom_window, recommendation_window
    messagebox.showinfo("Request Gaviscon", "Gaviscon can be obtained by contacting your admin to request a Doctor on : \n"
                                               "123456789")
    if symptom_window:
        symptom_window.destroy()
    if recommendation_window:
        recommendation_window.destroy()


def request_hydrocortisone_cream():
    global symptom_window, recommendation_window
    messagebox.showinfo("Request Hydrocortisone Cream", "Hydrocortisone Cream can be obtained by contacting your admin to request a Doctor on : \n"
                                               "123456789")
    if symptom_window:
        symptom_window.destroy()
    if recommendation_window:
        recommendation_window.destroy()


def request_doctor():
    global symptom_window, recommendation_window
    messagebox.showinfo("Request a Doctor", "To request a doctor, please call your Admin on: 123456789.")
    if symptom_window:
        symptom_window.destroy()
    if recommendation_window:
        recommendation_window.destroy()



def logout():
    global open_windows
    while open_windows:
        window = open_windows.pop()
        try:
            window.destroy()
        except:
            pass


def refugee_menu(manage_refugee):
    '''manage_refugee = tk.Tk()
    manage_refugee.title("Refugee Menu")
    manage_refugee.geometry("400x400")'''

    create_refugee_button = tk.Button(manage_refugee, text="Create Refugee", command=create_refugee)
    create_refugee_button.pack(pady=10)

    delete_refugee_button = tk.Button(manage_refugee, text="Delete Refugee", command=delete_refugee)
    delete_refugee_button.pack(pady=10)

    view_refugee_button = tk.Button(manage_refugee, text="View Refugee", command=view_refugee)
    view_refugee_button.pack(pady=10)

    search_refugee_button = tk.Button(manage_refugee, text="Search Refugee", command=search_refugee)
    search_refugee_button.pack(pady=10)

    edit_refugee_button = tk.Button(manage_refugee, text="Edit Refugee", command=edit_refugee)
    edit_refugee_button.pack(pady=10)

    view_family_button = tk.Button(manage_refugee, text="View All Family", command=view_by_family)
    view_family_button.pack(pady=10)

    search_family_button = tk.Button(manage_refugee, text="Search Family", command=search_family_menu)
    search_family_button.pack(pady=10)

    medic_attention_button = tk.Button(manage_refugee, text="Medic Attention", command=medic_attention)
    medic_attention_button.pack(pady=10)

    otc_med_button = tk.Button(manage_refugee, text="Request OTC Medication", command=request_otc_med)
    otc_med_button.pack(pady=10)

    manage_refugee.mainloop()

# refugee_menu()
# family()
