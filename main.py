import psycopg2
import database as db
import frontend as fe
from dotenv import load_dotenv
import os

"""
This file is responsible to interact with the user

- Error handling is made here
- This file is responsible for showing the menu to the user
"""


load_dotenv()

pw = os.getenv('postgres')

con = db.connect_db(pw)

first_run_text = """
Welcome to SellHouse App
- For first run You need to create an admin profile -
--> Press [0] to create an admin profile
"""

menu_text = """
Main Menu
Make a choice:
[0] = Admin
[1] = User
[2] = Broker
[q] = Quit the program
"""

admin_text = """
Admin Menu
Make a choice:
[0] = Add an admin
[1] = Create an announcement
[2] = Delete an announcement
[3] = View listings
[4] = Create a category
[5] = Update a category
[6] = View users
[7] = View brokers
[q] = Quit the admin menu
"""
admin_options = {
    '0': fe.add_admin,
    '1': fe.create_listing,
    '2': fe.delete_listing_admin,
    '3': fe.view_lists,
    '4': fe.create_category,
    '5': fe.update_category,
    '6': fe.list_users,
    '7': fe.list_brokers
}

users_text = """
Users Menu
Make a choice:
[0] = Add a user profile
[1] = Delete your profile
[2] = Create an announcement
[3] = Delete an announcement
[4] = View listings
[5] = View your favorite/unfavorite lists
[6] = Book an appointment
[7] = Cancel an appointment
[8] = Edit an appointment
[9] = Edit your profile
[q] = Quit the user menu
"""

users_options = {
    '0': fe.add_users,
    '1': fe.delete_user_profile,
    '2': fe.create_listing,
    '3': fe.delete_listing_user,
    '4': fe.view_lists,
    '5': fe.view_favorite_unfavorite_lists,
    '6': fe.book_appointment,
    '7': fe.cancel_appointment,
    '8': fe.update_appointment,
    '9': fe.update_user_profile
}

brokers_text = """
Brokers Menu
Make a choice:
[0] = Add a broker profile
[1] = Update your profile
[2] = Delete your profile
[3] = View your appointments
[q] = Quit the brokers menu
"""

brokers_options = {
    '0': fe.add_brokers,
    '1': fe.update_broker_profile,
    '2': fe.delete_broker_profile,
    '3': fe.view_appointments
}


def admin(con):
    check_password = fe.check_password(con)
    if not check_password:
        menu(con)
    elif check_password:
        print('You have entered')
        while True:
            try:
                choice = input(admin_text)
                if choice.upper() == 'Q':
                    break
                admin_options[choice](con)
                input("Press enter to continue")
            except Exception as e:
                print(e)
                print('Not a valid choice!')


def users(con):
    while True:
        try:
            choice = input(users_text)
            if choice.upper() == 'Q':
                break
            users_options[choice](con)
            input("Press enter to continue")
        except Exception as e:
            print(e)
            print('Not a valid choice!')


def brokers(con):
    while True:
        try:
            choice = input(brokers_text)
            if choice.upper() == 'Q':
                break
            brokers_options[choice](con)
            input("Press enter to continue")
        except Exception as e:
            print(e)
            print('Not a valid choice!')


def first_run(con):
    db.create_tables(con)
    try:
        choice = input(first_run_text)
        if choice == '0':
            admin_options[choice](con)
            input("Press enter to continue")
    except Exception as e:
        print(e)
        print('Not a valid choice!')


def menu(con):
    try:
        while True:
            choice = input(menu_text)
            if choice == '0':
                admin(con)
            elif choice == '1':
                users(con)
            elif choice == '2':
                brokers(con)
            elif choice.upper() == 'Q':
                print("SellHouse App: Thank you for using SellHouse App!")
                return False
            else:
                print('Not a valid choice!')
    except Exception as e:
        print(e)
        print('Not a valid choice!')


if __name__ == '__main__':
    try:
        con = db.connect_db(pw)
        try:
            first_run(con)
        except psycopg2.DatabaseError as e:
            pass
        while True:
            quit = menu(con)
            if not quit:
                exit()
    finally:
        con.close()