# For inputs that should be alphabets only
def num_input(inputType):
    inputDig = 0
    if inputType == 'campId':
        inputDig = input("Enter refugee campId: ")
    elif inputType == 'age':
        inputDig = input("Enter refugee age: ")
    elif inputType == 'psyHealth':
        inputDig = input("Enter refugee mental health (1-5): ")
    elif inputType == 'physHealth':
        inputDig = input("Enter refugee physical health (1-5): ")
    if numeric_check(inputDig):
        return inputDig
    else:
        print("\nInvalid input, please try again.")


def alpha_input(inputType):
    inputStr = ''
    if inputType == 'name':
        inputStr = input("Enter refugee name: ")
    elif inputType == 'surname':
        inputStr = input("Enter refugee surname: ")
    elif inputType == 'gender':
        inputStr = input("Enter refugee gender: ")
    elif inputType == 'bloodType':
        inputStr = input("Enter refugee bloodType: ")
    elif inputType == 'family':
        inputStr = input("Enter refugee family: ")
    elif inputType == 'language':
        inputStr = input("Enter refugee language: ")

    if alpha_check(inputStr):
        return inputStr


    else:
        print("\nInvalid input, please try again.")


# For campId: input should be digits only
def numeric_check(inputDig):
    if inputDig.isdigit() == True:
        return True
    else:
        return False


def age_check(inputDig):
    if inputDig.isdigit() and int(inputDig) < 150:
        return True
    else:
        return False


def alpha_check(inputStr):
    if inputStr.isalpha() == True:
        if inputStr.isalpha():
            return True
        else:
            return False


def bool_input(bool_input):
    if isinstance(bool_input, bool):
        return True
    else:
        return False