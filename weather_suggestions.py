

def check_temp(temperature):
    if temperature <= 0:
        return True, "Temperature at this location is below freezing, please consider allocating resources to accomodate this."
    elif temperature < -10:
        return False,  "Temperature at this location is below -10 degrees ceclius. This deemed unsuitable. Please select a different camp location."
    elif temperature >= 30 and temperature < 45:
        return True, "Temperature is above 30 degrees celsius at this location, please consider allocating resources to accomodate this."
    elif temperature >= 45:
        return False, "Temperature at this location is too hot. This is deemed unsuitable. Please select a different location"
    else:
        return True, "Weather is suitable at this location"
