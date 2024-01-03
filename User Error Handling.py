class InvalidLoginError(Exception):
    pass


class InvalidUsernameError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class InvalidNameError(Exception):
    pass


class InvalidSurnameError(Exception):
    pass


class InvalidPhoneNumberError(Exception):
    pass


class User:
    def __init__(self, username: str, password: str, name: str, surname: str, phone: str, user_type, status="active"):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.phone = phone
        self.user_type = user_type
        self.status = status

        try:
            if isinstance(name, str):
                raise InvalidNameError()
            if isinstance(surname, str):
                raise InvalidSurnameError()
            if len(phone) != 11:
                raise InvalidPhoneNumberError()     # raises an error if phone number is less than 11 digits
            if isinstance(phone, int):
                raise InvalidPhoneNumberError()
        except InvalidLoginError:
            print("Invalid Username or Password ")
        except InvalidPhoneNumberError:
            print(f"Invalid Phone Number: {phone}")
        except InvalidNameError:
            print("Name can not contain numbers")
        except InvalidSurnameError:
            print("Surname can not contain numbers")


class Admin(User):

    def __init__(self, username: str, password: str, name: str, surname: str,
                 phone: str, user_type="Admin", status="active"):
        super().__init__(username, password, name, surname, phone, user_type, status)

        try:
            if username != "admin":
                raise InvalidUsernameError()
            if password != "111":
                raise InvalidPasswordError()
            if isinstance(name, str):
                raise InvalidNameError()
            if isinstance(surname, str):
                raise InvalidSurnameError()
            if len(phone) != 11:
                raise InvalidPhoneNumberError()
            if isinstance(phone, int):
                raise InvalidPhoneNumberError()
        except InvalidUsernameError:
            print("Invalid Username")
        except InvalidPasswordError:
            print("Incorrect Password")
        except InvalidPhoneNumberError:
            print(f"Invalid Phone Number: {phone}")
        except InvalidNameError:
            print("Name cannot contain numbers")
        except InvalidSurnameError:
            print("Surname cannot contain numbers")


volunteer_usernames = ["volunteer1", "volunteer2", "volunteer3"]


class Volunteer(User):
    def __init__(self, username: str, password: str, name: str, surname: str,
                 phone: str, camp_id: str, availability: str, user_type="volunteer", status="active"):
        super().__init__(username, password, name, surname, phone, user_type, status)

        self.camp_id = camp_id

        try:
            if username != "admin":
                raise InvalidUsernameError()
            if password != "111":
                raise InvalidPasswordError()
            if isinstance(name, str):
                raise InvalidNameError()
            if isinstance(surname, str):
                raise InvalidSurnameError()
            if len(phone) != 11:
                raise InvalidPhoneNumberError()
            if isinstance(phone, int):
                raise InvalidPhoneNumberError
        except InvalidUsernameError:
            print("Invalid Username")
        except InvalidPasswordError:
            print("Incorrect Password")
        except InvalidPhoneNumberError:
            print(f"Invalid Phone Number: {phone}")
        except InvalidNameError:
            print("Name cannot contain numbers")
        except InvalidSurnameError:
            print("Surname cannot contain numbers")
