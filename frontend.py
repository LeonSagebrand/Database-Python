"""This file is responsible for taking information from the menu and send it to the database for CRUD in backend"""
import psycopg2
import database as db


# -----------------------------------------Admin Functions------------------------------------------------------------ #


def check_password(con):
    password = input('Enter your password: ')
    try:
        db.check_password_db(con=con, password=password)
        return True
    except Exception as e:
        print('Wrong password!')
        return False


def add_admin(con):
    """This function is used to add an admin to the database"""
    print('- Adding an admin -')
    first_name = input('First name: ')
    last_name = input('Last name: ')
    phone_number = input('Phone number: ')
    password = input('Create a password: ')
    email = input('Email: ')
    admin = True
    try:
        db.add_users_db(con=con, first_name=first_name, last_name=last_name, phone_number=phone_number,
                        email=email, password=password, admin=admin)
        print('Successfully added an admin!')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def create_listing(con):
    """- This function is common to admins and users
    - This function is to create a new listing"""
    print('- Adding an announcement -')
    password = input("Enter your password: ")
    try:
        db.check_password_db(con=con, password=password)
    except Exception as e:
        print('Wrong password!')
        return
    print("Which broker would you like to have?")
    column_names, choices = db.choosing_broker_db(con)
    print(column_names)
    for choice in choices:
        print(choice)
    user_choice = input("Enter the broker's id for the broker here: ")
    category = input('What type of house are you selling? ')
    address = input('Enter the address: ')
    municipality = input('Which kommun is the house in: ')
    postal_code = input('Postal Code: ')
    size = input('Size: ')
    number_of_rooms = input('Number of rooms: ')
    year_of_construction = input('Year of construction: ')
    description = input('Description: ')
    price = input('What is the price of the house? ')
    balcony = input('Is there a balcony? ')
    elevator = input('Is there a an elevator? ')

    try:
        db.add_listing_db(con=con, password=password, broker_id=user_choice, category=category, address=address,
                          municipality=municipality,
                          postal_code=postal_code, size=size, number_of_rooms=number_of_rooms,
                          year_of_construction=year_of_construction, description=description, price=price,
                          balcony=balcony, elevator=elevator)
        print('Successfully added')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def delete_listing_admin(con):
    print('- Deleting an announcement -')
    print('Which announcement would you like to delete?')
    column_names, choices = db.list_lists_db(con=con)
    print(column_names)
    for choice in choices:
        print(choice)
    user_choice = input("Enter the list's id here to delete: ")
    try:
        db.delete_list_admin_db(con=con, list_id=user_choice)
        print('Successfully deleted!')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def view_lists(con):
    """- This function is common to admins and users
    - This also allows users to add a list into their favorite/unfavorite lists"""
    print('- Viewing lists -')
    try:
        column_names, lists = db.list_lists_db(con=con)
        print(column_names)
        for list in lists:
            print(list)
        add_favorite_list = input("Would you like to add a favorite listing? Y/N: ")
        if add_favorite_list.upper() == "Y":
            user_choice = input("Enter the list's id here to add it to your Favorite/Unfavorite lists: ")
            password = input("Enter your password: ")
            try:
                db.check_password_db(con=con, password=password)
            except Exception as e:
                print('Wrong password!')
                return
            try:
                db.add_favorite_unfavorites_lists_db(con=con, password=password, list_id=user_choice,
                                                     like_dislike=like_dislike())
                print('Successfully added to your favorite/unfavorite lists')
            except psycopg2.DatabaseError as e:
                print('Something went wrong!')
                print("You have already liked/disliked this announcement before!")
                return False
        elif add_favorite_list.upper() == "N":
            return False
        else:
            print('Not a valid choice!.')
            return False
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def create_category(con):
    print('- Adding a category -')
    type_name = input('Enter the category name: ')
    try:
        db.add_category_db(con=con, type_name=type_name)
        print('Successfully added!')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)
        return False


def update_category(con):
    print('- Updating a category -')
    print('Which category would you like to update?')
    column_names, choices = db.list_category_db(con=con)
    print(column_names)
    for choice in choices:
        print(choice)
    user_choice = input("Enter the category's id here: ")
    new_type_name = input('What is the new type name? ')
    try:
        db.update_category_db(con=con, new_type_name=new_type_name, type_id=user_choice)
        print('Successfully updated!')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def list_users(con):
    print('- Viewing users -')
    try:
        column_names, users = db.list_users_db(con=con)
        print(column_names)
        for user in users:
            print(user)
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def list_brokers(con):
    print('- Viewing brokers -')
    try:
        column_names, brokers = db.list_brokers_db(con=con)
        print(column_names)
        for broker in brokers:
            print(broker)
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


# -----------------------------------------Users Functions------------------------------------------------------------ #


def add_users(con):
    print('- Adding a user -')
    first_name = input('First name: ')
    last_name = input('Last name: ')
    phone_number = input('Phone number: ')
    password = input('Create a password: ')
    email = input('Email: ')
    admin = False
    try:
        db.add_users_db(con=con, first_name=first_name, last_name=last_name, phone_number=phone_number,
                        email=email, password=password, admin=admin)
        print('Successfully added the user!')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def delete_user_profile(con):
    print('- Deleting a user profile -')
    password = input('Enter your password to delete your profile: ')
    try:
        db.check_password_db(con=con, password=password)
        print('Successfully deleted!')
    except Exception as e:
        print('Wrong password!')
        return
    try:
        db.delete_user_profile_db(con=con, password=password)
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def delete_listing_user(con):
    """- This function is used to show the user's own listings to delete.
    - They cannot see the other listings made by the other users to delete."""
    print('- Deleting your announcement -')
    password = input('Enter your password here: ')
    try:
        db.check_password_db(con=con, password=password)
    except Exception as e:
        print('Wrong password!')
        return
    print('Which announcement would you like to delete?')
    column_names, choices = db.user_lists_db(con=con, password=password)
    print(column_names)
    for choice in choices:
        print(choice)
    user_choice = input("Enter the list's id here to delete: ")
    try:
        db.delete_list_user_db(con=con, list_id=user_choice, password=password)
        print('Successfully deleted!')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def like_dislike():
    like_dislike = input("Make a choice:\n"
                         "[1] = Like\n"
                         "[2] = Dislike\n")
    if like_dislike == '1':
        return True
    elif like_dislike == '2':
        return False
    else:
        print("Invalid choice!")


def favorite_unfavorite():
    print('Do you want to see your Liked or Disliked lists?')
    liked_disliked = input("Make a choice:\n"
                           "[1] = View your favorites lists\n"
                           "[2] = View your unfavorites lists\n")
    if liked_disliked == '1':
        return True
    elif liked_disliked == '2':
        return False
    else:
        print("Invalid choice!")


def view_favorite_unfavorite_lists(con):
    print('- Viewing your liked/disliked lists -')
    password = input("Enter your password here: ")
    try:
        db.check_password_db(con=con, password=password)
    except Exception as e:
        print('Wrong password!')
        return
    try:
        column_names, choices = db.view_favorite_unfavorite_lists_db(con=con, password=password, liked_disliked=favorite_unfavorite())
        print(column_names)
        for choice in choices:
            print(choice)
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def book_appointment(con):
    print('- Booking an appointment -')
    password = input('Enter your password: ')
    try:
        db.check_password_db(con=con, password=password)
    except Exception as e:
        print('Wrong password!')
        return
    print('Which announcement would you like to book an appointment?')
    column_names, choices = db.list_lists_db(con=con)
    print(column_names)
    for choice in choices:
        print(choice)
    user_choice = input("Enter list's id here: ")
    visit_date = input("Enter the date for appointment: ")
    try:
        db.book_appointment_db(con=con, password=password, broker_id=user_choice, visit_date=visit_date)
        print('Appointment has been added successfully!')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def cancel_appointment(con):
    print('- Canceling your appointments -')
    password = input('Enter your password: ')
    try:
        db.check_password_db(con=con, password=password)
    except Exception as e:
        print('Wrong password!')
        return
    print('Which appointment would you like to cancel?')
    column_names, choices = db.view_appointments_user_db(con=con, password=password)
    print(column_names)
    for choice in choices:
        print(choice)
    user_choice = input("Enter appointment's id here: ")
    try:
        db.cancel_appointment_db(con=con, appointment_id=user_choice)
        print("Successfully cancelled the appointment!")
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def update_appointment(con):
    print('- Updating your appointments date -')
    password = input("Enter your password: ")
    try:
        db.check_password_db(con=con, password=password)
    except Exception as e:
        print('Wrong password!')
        return
    print('Choose the appointment that you would like to change the date for it:')
    column_names, choices = db.view_appointments_user_db(con=con, password=password)
    print(column_names)
    for choice in choices:
        print(choice)
    user_choice = input("Enter appointment's id here: ")
    new_visit_date = input("Enter your appointment date: ")
    try:
        db.update_appointment_db(con=con, new_visit_date=new_visit_date, appointment_id=user_choice)
        print("Your appointment date has been updated.")
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def update_user_profile(con):
    print('- Updating your profile password -')
    password = input("Enter your password: ")
    try:
        db.check_password_db(con=con, password=password)
    except Exception as e:
        print('Wrong password!')
        return
    new_password = input("Enter your new password: ")
    try:
        db.update_user_profile_db(con=con, new_password=new_password, password=password)
        print("Your new password has been updated.")
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


# -----------------------------------------Brokers Functions---------------------------------------------------------- #


def add_brokers(con):
    print('- Adding a broker -')
    first_name = input('First name: ')
    last_name = input('Last name: ')
    phone_number = input('Phone number: ')
    try:
        db.add_brokers_db(con=con, first_name=first_name, last_name=last_name, phone_number=phone_number)
        print('Successfully added a broker!')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)
        return False


def update_broker_profile(con):
    print('- Updating your profile phone number -')
    phone_number = input("Enter your phone number: ")
    new_phone_number = input("Enter your new phone number: ")
    try:
        db.update_broker_profile_db(con=con, new_phone_number=new_phone_number, phone_number=phone_number)
        print('Your new phone number has been updated.')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)


def delete_broker_profile(con):
    print('- Deleting your profile -')
    phone_number = input("Enter your phone number delete your profile: ")
    try:
        db.delete_broker_profile_db(con=con, phone_number=phone_number)
        print('Your profile has been deleted successfully.')
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print("Can't delete a broker if an appointment has been booked with this profile")


def view_appointments(con):
    print('- Viewing your appointments -')
    phone_number = input("Enter your phone number: ")
    try:
        column_names, choices = db.view_appointments_broker_db(con=con, phone_number=phone_number)
        print(column_names)
        for choice in choices:
            print(choice)
    except psycopg2.DatabaseError as e:
        print('Something went wrong!')
        print(e)