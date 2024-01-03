class InvalidAgeError(Exception):
    pass


class InvalidNameError(Exception):
    pass


class InvalidSurnameError(Exception):
    pass


class InvalidCampIdError(Exception):
    pass


class InvalidLanguageError(Exception):
    pass


gender_directory = ["Male", "Female", "Other"]
# think it's best to have this as a drop-down menu with the option to add something else when other is clicked


class InvalidGenderError(Exception):
    pass


blood_type_directory = ["A+", "A-", "AB+", "AB-", "B+", "B-", "O+", "O-"]
# again a drop-down menu would be best for this


class InvalidBloodTypeError(Exception):
    pass


class InvalidRefugeeIdError(Exception):
    pass


class InvalidHealthScoreError(Exception):
    pass


family_list = []


class InvalidFamilyError(Exception):
    pass


class Refugee:

    def __init__(self, name: str, surname: str, camp_id: str, age: str, languages: str, gender: str,
                 blood_type: str, psych_health: str, phys_health: str, family: str, refugee_id=None):

        self.name = name
        self.surname = surname
        self.camp_id = camp_id
        self.age = age
        self.languages = languages
        self.gender = gender
        self.blood_type = blood_type
        self.psych_health = psych_health
        self.phys_health = phys_health
        self.family = family
        self.refugee_id = refugee_id

        try:
            if isinstance(refugee_id, int):
                raise InvalidRefugeeIdError
            if isinstance(name, str):
                raise InvalidNameError()
            if isinstance(surname, str):
                raise InvalidSurnameError()
            if isinstance(camp_id, int):
                raise InvalidCampIdError
            if camp_id <= 0:
                raise ValueError("Camp Id must be a positive integer")
            if isinstance(languages, str):
                raise InvalidLanguageError()
            if blood_type not in blood_type_directory:
                raise InvalidBloodTypeError()
            if phys_health not in range(1, 11):         # scoring health on a scale from 1 to 10
                raise InvalidHealthScoreError()
            if isinstance(phys_health, int):
                raise InvalidHealthScoreError()
            if psych_health not in range(1, 11):
                raise InvalidHealthScoreError()
            if isinstance(psych_health, int):
                raise InvalidHealthScoreError()
            if family not in family_list:
                raise InvalidFamilyError
        except InvalidRefugeeIdError:
            print(f"Invalid Refugee ID: {refugee_id}")
        except InvalidNameError:
            print("Name cannot contain numbers")
        except InvalidSurnameError:
            print("Surname cannot contain numbers")
        except InvalidCampIdError:
            print(f"Invalid Camp ID: {camp_id}")
        except InvalidLanguageError:
            print(f"Invalid Language: {languages}")
        except InvalidBloodTypeError:
            print(f"Invalid Blood Type: {blood_type}")
        except InvalidHealthScoreError:
            print(f"Invalid Health Score: {phys_health}, Please input a number between 1 and 10")
        except InvalidFamilyError:
            print(f"Invalid Family: {family}")
