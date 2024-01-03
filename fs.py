# functions library
import hashlib as hl

# Hash the password to improve security with built-in hashlib library
def hash_password(pw):
    hashObject = hl.sha256()
    hashObject.update(pw.encode('utf-8'))
    hashedPw = hashObject.hexdigest()

    return hashedPw

def table_exists(table_name, connection):
    cursor = connection.cursor()

    # Execute a query to check if the table exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")

    # Fetch the result
    result = cursor.fetchone()

    # If result is not None, the table exists
    if result:
        return True
    else:
        return False

# Check if the 'phone' and 'camp_id' only contains numbers
def check_numeric(attribute):
    while True:
        # userInput = input("Enter new volunteer's " + attribute + ": ")
        if attribute.isdigit():
            return attribute
        else:
            print("Invalid input")

# easier input for user
def bool_input(prompt):
    while True:
        user_input = input(f"{prompt} (yes/no): ").lower()
        if user_input == "yes":
            return True
        elif user_input == "no":
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")