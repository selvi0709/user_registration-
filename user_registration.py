import json
import os
from jsonschema import validate

email_schema = {
    "type": "string",
    "pattern": "(^[A-Za-z])([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
}
password_schema = {
    "type": "string",
    "pattern": "^((?=.*[a-z]){1})((?=.*[A-Z]){1})(?=.*\d)((?=.*[!@#$%^&*()\-_=+{};:,<.>]){1})[A-Za-z\d!@#$%^&*("
               ")\-_=+{};:,<.>]{5,16}$"
}


def user_read():
    """
    This method is used to fetch the user details from the file
    :return: User data will be returned in dict format
    """
    with open('user.json', 'r+') as f:
        data_dict = json.load(f)
    return data_dict


def user_create(user):
    """
    This method is used for user creation
    :param user: name of the user
    :return: True if user created successfully
    """
    with open('user.json', 'r+') as f:
        info = user_read()
        info.update(user)
        json.dump(info, f, indent=4)
    return True


def user_register():
    """
    This method is used to register the newly created user
    """
    user = {}
    email = input("Enter email: ")
    pwd = input("Enter password: ")
    try:
        validate(email, email_schema)
        validate(pwd, password_schema)
        user.update({email: pwd})
        if user_create(user):
            print(f"User {email} added successfully in the user_file")
        else:
            print(f"Problem in creating the {email} user")
    except Exception as e:
        print("Data Insertion failed {}".format(e))


def user_login(name, pwd=None, user_check=None):
    """
    This method is used for user login
    :param name: name of the user
    :param pwd: password of the user
    :param user_check: (optional)
    :return: "success" for successful login, "fail" for unsuccessful login
    """
    user_list = user_read()
    for k, v in user_list.items():
        if k == name:
            if user_check:
                return True
        if k == name:
            if v == pwd:
                return "success"
            else:
                print("Incorrect password")
                return "fail"


def user_exists(name):
    """
    This method is used to check if the user already exists in the file
    :param name: name of the user
    :return: True if user exists
    """
    if user_login(name, pwd=None, user_check=True):
        return True


def user_update(name, new_pwd):
    """
    This method is used to update the user credentials
    :param name: name of the user
    :param new_pwd: user's new password to update in the file
    :return: True if updated successfully
    """
    try:
        user_list = user_read()
        for k in user_list.keys():
            if k == name:
                validate(new_pwd, password_schema)
                user_list.update({name: new_pwd})
                with open('user.json', 'w') as f:
                    json.dump(user_list, f, indent=4)
                return True
    except Exception as e:
        print("Password updating failed {}".format(e))


if __name__ == '__main__':
    if not os.path.isfile('./user.json'):
        with open('user.json', 'w') as f:
            json.dump({"dummy@gmail.com": "Dummy@123"}, f, indent=4)
    print("Press option 1 for Login")
    print("Press option 2 for Forgot password")
    print("Press option 3 for New Registration")
    print("Press option 4 for Exit")
    option = int(input("Enter option: "))
    opt = 0
    if option == 1:
        print("Enter login credentials")
        name = input("Enter username: ")
        pwd = input("Enter password: ")
        status = user_login(name, pwd)
        if status == "success":
            print("User logged in successfully")
        elif status == "fail":
            print("Returning to Home page")
        else:
            print("User does not exist")
            action = input("Would you like to register(yes/no): ")
            if action == "yes":
                opt = int(input("Enter option 3 for Register: "))
            else:
                print("Returning to Home page")

    elif option == 2:
        print("Enter user credentials")
        name = input("Enter username: ")
        if user_exists(name):
            new_pwd = input("Enter new password to change: ")
            if user_update(name, new_pwd):
                print("Password updated successfully")
        else:
            print("User does not exists")
            action = input("Would you like to register(yes/no): ")
            if action == "yes":
                opt = int(input("Enter option 3 for Register: "))
            else:
                print("Returning to Home page")

    elif option == 3:
        user_register()

    elif option == 4:
        exit()

    if opt == 3:
        user_register()
