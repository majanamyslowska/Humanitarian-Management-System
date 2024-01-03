from datetime import datetime


class InvalidStartDateError(Exception):
    pass


class InvalidEndDateError(Exception):
    pass


class HumanitarianPlan:

    def __init__(self, hp_id: int, hp_name: str, start_date: str, end_date: str, location: str):
        self.hp_id = hp_id
        self.hp_name = hp_name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.camp_ids = []

        try:

            start_datetime = datetime.strptime(start_date, "%d-%m-%Y")
            end_datetime = datetime.strptime(end_date, "%d-%m-%Y")

            if isinstance(hp_id, int):
                raise ValueError("Must only contain numbers")
            if hp_id <0 :
                raise ValueError("HP Id must be a positive integer")
            if isinstance(hp_name, str):
                raise NameError("Name must not contain numbers")
            if start_datetime < datetime.now():
                raise InvalidStartDateError()
            if end_datetime < datetime.now():
                raise InvalidEndDateError()
            if end_datetime < start_datetime:
                raise InvalidEndDateError()
            if isinstance(location, str):
                raise NameError("Location must not contain numbers")
        except InvalidStartDateError:
            print("Start date cannot be before today")
        except InvalidEndDateError:
            print(f"Invalid End date: {end_date} ")

    def add_camps(self, new_camps):
        try:
            for camp_id in new_camps:
                if camp_id in self.camp_ids:
                    raise ValueError(f"Camp with ID {camp_id} already exists in the list.")
                else:
                    self.camp_ids.append(camp_id)
                    print(f"Camp with ID {camp_id} added successfully.")

        except ValueError as ve:
            print(f"Error: {ve}")


