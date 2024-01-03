class Camp:

    def __init__(self, camp_id: int, capacity: int, resources_state: str):
        self.camp_id = camp_id
        self.capacity = capacity
        self.resources_state = resources_state
        self.resources = []
        self.refugees_ids = []
        self.volunteers_ids = []

        try:
            if isinstance(camp_id, int):
                raise TypeError("Camp Id must be integers")
            if camp_id <= 0 :
                raise ValueError("Camp ID must be a positive integer")
            if isinstance(capacity, int):
                raise TypeError(f"Invalid Capacity: {capacity}")
            if capacity <= 0:
                raise ValueError("Invalid capacity. Capacity must be a positive integer.")
        except TypeError or ValueError as e:
            print(f"Error initialising Camp: {e}")

