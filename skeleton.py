''' ________________________________DATA________________________________'''

admin = ''
volunteers = []
refugees = []
camps = []
plans = []
resources = []

''' ________________________________CLASSES________________________________'''


class User:

    def __init__(self, username: str, password: int):
        self.username = username
        self.password = password

    def login(self):
        # check if the combination of username+password is in volunteers array or is admin
        # display the role that a person logged as
        pass

    def logout(self):
        # every now and then give someone an option to logout?
        # display info that you logged out and guve an option to log in again
        pass


class Admin(User):

    def __init__(self, username: str, password: str, name: str, surname: str, age: int, phone_no: int):
        super().__init__(username, password)
        self.name = name
        self.surname = surname
        self.age = age
        self.phone_no = phone_no


class Volunteer(User):

    def __init__(self, username: str, password: str, name: str, surname: str, v_id: int, age: int, phone_no: int,
                 camp_id: int, languages: list, bloodtype: str, status: str):
        super().__init__(username, password)
        self.name = name
        self.surname = surname
        self.v_id = v_id
        self.age = age
        self.phone_no = phone_no
        self.camp_id = camp_id
        self.languages = languages
        self.bloodtype = bloodtype
        self.status = status

    def __str__(self):
        pass
        # return f'Volunteer {self.v_id} information: Name: {}, Surname: {} etc ...'

    def edit_status(self):
        # method used by an ADMIN
        # input what u want to change eg. deactivate
        pass


class HumanitarianPlan:

    def __init__(self, hp_id: int, hp_name: str, start_date: str, end_date: str, location: str):
        self.hp_id = hp_id
        self.hp_name = hp_name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.camp_ids = []

    def add_camps(self):
        pass
        # add camps to the list

    def __str__(self):
        # return f'{self.hp_name} is located in {self.location}, started on ...'
        pass

    def create_new_hp(self):
        # method used by an ADMIN
        pass

    def end_hp(self):
        # method used by an ADMIN
        pass


class Camp:

    def __init__(self, camp_id: int, capacity: int, resources_state: str):
        self.camp_id = camp_id
        self.capacity = capacity
        self.resources_state = resources_state
        self.resources = []
        self.refugees_ids = []
        self.volunteers_ids = []

    def __str__(self):
        # return f'Camp {self.camp_id} is has the capacity of ...'
        pass

    def add_r_to_camp(self):
        # method used by an ADMIN
        pass

    def add_v_to_camp(self):
        # method used by an ADMIN
        pass

    def edit_camp_info(self):
        # based on input what u want to change eg. capacity
        # call by key capacity and change it (if statements)
        pass

    def allocate_resources(self):
        # method used by an ADMIN
        # input resources
        # decide on an algorithm for allocating resources - size of the camp, allergies etc
        # update camp info - call edit_camp_info
        pass


class Refugee:

    def __init__(self, refugee_id: int, name: str, surname: str, camp_id: int, age: int, languages: list,
                 bloodtype: str, psych_health: int, phys_health: dict, family: list):
        self.refugee_id = refugee_id
        self.name = name
        self.surname = surname
        self.camp_id = camp_id
        self.age = age
        self.languages = languages
        self.bloodtype = bloodtype
        self.psych_health = psych_health
        self.phys_health = phys_health
        self.family = family

    def __str__(self):
        # return f'Refugee {self.refugee_id} information: Name: {}, Surname: {} etc ...'
        pass

    def add_refugee(self):
        # method used by a VOLUNTEER
        # based on the input add a new refugee
        pass


class Resources:

    def __init__(self, resource_type: str, total_amount: int):
        self.resource_type = resource_type
        self.total_amount = total_amount

    def update_rs(self):
        # inventory; linked to allocate_resources f
        pass


''' ________________________________RUN________________________________'''

# admin = Admin()

'''populate volunteers, plans, camps, refugees, resources
v1 = Volunteer() # ... v1-v20
volunteers.append(v1)

r1 = Refugee() # ... r1-r20
refugees.append(r1)

c1 = Camp() # ... c1-c10
camps.append(c1)

hp1 = HumanitarianPlan() # ... hp1-hp3
plans.append(hp1)

'''

''' ________________________________TESTS________________________________'''


def main_menu():
    '''prints a menu of options at each step: are u the admin of volunteer, press 0 for admin, 1 for volunteer. once clicked
    which one login options, so input username and password, then ask what you want to do: list of a/v functionalities, depending on their first choice
    then on and on.

    this function is for all the ifs and displays, eg.:
    if you want to display hp info, press 1:
    if pressed one, call function __str__ in class hp
    it should show info about the plan and ask smth like do u want specific info on any of the camps etc OR GO BACK'''
