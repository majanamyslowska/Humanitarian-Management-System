import tkinter as tk
from tkinter import messagebox

symptoms = ["Pain", "Inflammation", "Cough", "Fever", "Allergic Reaction", "Indigestion", "Itchy Skin"]

symptoms_vars = []
other_var = None


def show_symptoms_page():
    root.withdraw()
    symptoms_page()


def symptoms_page():
    global symptoms_vars, other_var
    symptoms_vars = [tk.IntVar() for _ in symptoms]

    symptom_window = tk.Toplevel(root)
    symptom_window.title("Symptom Table")

    message_label = tk.Label(symptom_window, text="Please check the box if they only have these symptoms"
                                                  "\n otherwise, click 'Other'.")
    message_label.grid(row=0, columnspan=2, pady=20)

    labels = [tk.Label(symptom_window, text=symptom) for symptom in symptoms]

    check_buttons = [tk.Checkbutton(symptom_window, variable=symptom_var) for symptom_var in symptoms_vars]

    for label, check_button in zip(labels, check_buttons):
        label.grid(row=labels.index(label) + 1, column=0, padx=10, pady=10, sticky=tk.W)
        check_button.grid(row=labels.index(label) + 1, column=1, padx=10, pady=10, sticky=tk.W)

    other_var = tk.IntVar()
    other_checkbox = tk.Checkbutton(symptom_window, text="Other", variable=other_var,
                                    command=lambda: unselect_other_symptoms(other_var))
    other_checkbox.grid(row=len(symptoms) + 1, columnspan=2, pady=10)

    submit_button = tk.Button(symptom_window, text="Submit", command=lambda: submit(symptoms_vars, other_var))
    submit_button.grid(row=len(symptoms) + 2, columnspan=2, pady=10)


def unselect_other_symptoms(other_var):
    if other_var.get() == 1:
        for var in symptoms_vars[:]:
            var.set(0)


def submit(symptoms_vars, other_var):
    selected_symptoms = [symptom_var.get() for symptom_var in symptoms_vars]

    recommendations = []

    while selected_symptoms[3] == 0:
        if selected_symptoms[0] == 1:
            recommendations.append("For pain: take two 500mg paracetamol every 4 hours, 4 times a day.")
        if selected_symptoms[1] == 1:
            recommendations.append("For inflammation: take a 200mg tablet of ibuprofen every 6 hours.")
        if selected_symptoms[2] == 1:
            recommendations.append("For the cough: take cough syrup and follow the instructions on the bottle.")
        if selected_symptoms[4] == 1:
            recommendations.append("For the allergic reaction: take a 10mg tablet of Cetrizine once a day.")
        if selected_symptoms[5] == 1:
            recommendations.append("For indigestion: take Gaviscon.")
        if selected_symptoms[6] == 1:
            recommendations.append("For itchy skin: Use hydrocortisone cream once a day.")
        if other_var.get() == 1:
            recommendations.append("Please go see a Doctor")

    if selected_symptoms[3] == 1 and selected_symptoms[0]:
        recommendations.append("For the pain and fever: take two 500mg paracetamol every 4 hours, 4 times a day.")
    elif selected_symptoms[3] == 1:
        recommendations.append("For the fever: take two 500mg paracetamol every 4 hours, 4 times a day.")

    if recommendations:
        display_recommendations(recommendations)
    else:
        messagebox.showinfo("No Symptoms Selected", "No symptoms selected.")


def display_recommendations(recommendations):
    recommendation_window = tk.Toplevel(root)

    recommendation_window.geometry("500x100")

    recommendations_label = tk.Label(recommendation_window, text="Recommendations:")
    recommendations_label.pack()

    for recommendation in recommendations:
        recommendation_text = tk.Label(recommendation_window, text="- " + recommendation)
        recommendation_text.pack()

    if other_var.get() == 1:
        request_doctor_button = tk.Button(recommendation_window, text="Request a Doctor", command=request_doctor)
        request_doctor_button.pack()


def request_doctor():
    messagebox.showinfo("Request a Doctor", "A doctor will be notified. Please wait for assistance.")
    # Ideally want to send a message to the admin so they can approve it


root = tk.Tk()
root.title("Medical Health Check")


def yes_button_action():
    show_symptoms_page()


def no_button_action():
    root.destroy()


question_label = tk.Label(root, text="Does the refugee require medical assistance?")
question_label.grid(row=0, columnspan=2, pady=20)

yes_button = tk.Button(root, text="Yes", command=yes_button_action)
yes_button.grid(row=1, column=0, padx=10, pady=10)

no_button = tk.Button(root, text="No", command=no_button_action)
no_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
