from flask import Flask, request
from dotenv import load_dotenv
import os
import psycopg2
import database as db

app = Flask(__name__)
load_dotenv()
pw = os.getenv('DATABASE_PASSWORD')
con = db.connect_db(pw)

# Flask Endpoints


@app.route("/add_listing", methods=['POST'])
def add_listing():
    """
        Endpoint to add a new listing
    """
    password = 'iman'
    broker_id = '1'
    category = 'house'
    municipality = 'avesta'
    address = 'Hanstavägen 49'
    postal_code = '12345'
    size = '44'
    number_of_rooms = '2'
    year_of_construction = '2011'
    description = 'This is a good house'
    price = '1985000'
    balcony = 'yes'
    elevator = 'no'
    try:
        db.add_listing_db(con, password, broker_id, category, municipality, address, postal_code, size,
                          number_of_rooms, year_of_construction, description, price, balcony, elevator)
        return {'message': f'The announcement with address: {address} has been Successfully added'}, 200
    except psycopg2.DatabaseError:
        return {'message': f'Failed to add the announcement with address: {address}'}, 400


@app.route("/remove_listing", methods=['DELETE'])
def remove_listing():
    """
    Endpoint to remove a listing
    """
    list_id = '2'
    try:
        db.delete_list_admin_db(con, list_id)
        return {'message': f'list_id: {list_id} has been successfully deleted!'}, 200
    except psycopg2.DatabaseError:
        return {'message': f'Failed to delete list_id: {list_id}'}, 400


@app.route("/listing_detail", methods=['GET'])
def listing_detail():
    """
    Endpoint to return a specific listing
    """
    password = 'iman1'
    try:
        column_names, lists = db.user_lists_db(con, password)
        if not lists:
            return {'message': 'Failed to retrieve all your lists (Wrong Password)'}, 401
        else:
            return {'message': lists}, 200
    except psycopg2.DatabaseError:
        return {'message': 'Getl all lists failed'}, 500


@app.route("/get_all_listings", methods=['GET'])
def get_all_listings():
    """
    Should return a list of X number of listings based on a LIMIT
    """
    try:
        lists = db.list_lists_db(con)
        return {'message': lists}, 200
    except psycopg2.DatabaseError:
        return {'message': 'Getl all lists failed'}, 500


@app.route("/add_category", methods=['POST'])
def add_category():
    """
    Endpoint to add a new category
    Get category details from customer and call db.create_category
    """
    type_name = 'Plots'
    try:
        db.add_category_db(con, type_name)
        return {'message': f'category: {type_name} has been successfully added'}, 200
    except psycopg2.DatabaseError:
        return {'message': f'Failed to add category: {type_name}'}, 400


@app.route("/update_category", methods=['PUT'])
def update_category():
    """
    Endpoint to update a category
    Get updated category details from customer and call db.update_category
    """
    type_id = '1'
    type_name = 'Plots 2'
    try:
        db.update_category_db(con, type_name, type_id)
        return {'message': f'category: {type_name} has been successfully updated'}, 200
    except psycopg2.DatabaseError:
        return {'message': f'Failed update category: {type_name}'}, 400


@app.route("/add_broker", methods=['POST'])
def add_broker():
    """
    Endpoint to add a new broker
    Get broker details from customer and call db.create_broker
    """
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = data['phone_number']
    try:
        db.add_brokers_db(con, first_name, last_name, phone_number)
        return {'message': f'The broker: {first_name} {last_name} has been successfully added'}, 200
    except psycopg2.DatabaseError:
        return {'message': f'Failed to add broker: {first_name} {last_name}'}, 400


@app.route("/modify_broker", methods=['PUT'])
def modify_broker():
    """
    Endpoint to modify a broker
    Get updated broker details from customer and call db.update_broker
    """
    phone_number = '709997931'
    new_phone_number = 'test'
    try:
        db.update_broker_profile_db(con, new_phone_number, phone_number)
        return {'message': f'Phone number {phone_number} has been updated to {new_phone_number}'}, 200
    except psycopg2.DatabaseError:
        return {'message': f'Failed to update phone number {phone_number}'}, 400


@app.route("/add_customer", methods=['POST'])
def add_customer():
    """
    Endpoint to add a new customer
    Get customer details from customer and call db.create_customer
    """
    first_name = 'Test first name'
    last_name = 'Test last name'
    phone_number = 'Test phone number'
    email = 'Test email'
    password = 'test password'
    admin = False
    try:
        db.add_users_db(con, first_name, last_name, phone_number, email, password, admin)
        return {'message': f'The customer: {first_name} {last_name} has been successfully added'}, 200
    except psycopg2.DatabaseError:
        return {'message': f'Failed to add the customer: {first_name} {last_name}'}, 400


@app.route("/remove_customer", methods=['DELETE'])
def remove_customer():
    """
    Endpoint to remove a customer
    Get customer ID from customer and call db.delete_customer
    """
    password = 'test1'
    try:
        user_id = db.delete_user_profile_db(con, password)
        return {'message': f'The customer with user_id: {user_id} and password: {password} has been successfully '
                           f'deleted'}, 200
    except TypeError:
        return {'message': 'Failed to delete your profile (Wrong Password)'}, 401
    except psycopg2.DatabaseError:
        return {'message': f'Failed to delete the user'}, 400


@app.route("/get_all_customers", methods=['GET'])
def get_all_customers():
    """
    Endpoint to list all customer
    """
    try:
        users = db.list_users_db(con)
        return {'message': users}, 200
    except psycopg2.DatabaseError:
        return {'message': 'Failed to retrieve all customers'}, 400


@app.route("/schedule_appointment", methods=['POST'])
def schedule_appointment():
    """
    Endpoint to schedule a viewing appointment
    Get appointment details from customer and call db.create_appointment
    """
    password = 'test'
    list_id = '6'
    visit_date = '2030-01-21'
    try:
        db.book_appointment_db(con, password, list_id, visit_date)
        return {'message': f'The appointment with list_id: {list_id} has been successfully added with date: '
                           f'{visit_date}'}, 200
    except psycopg2.DatabaseError:
        return {'message': 'Failed'}, 400


@app.route("/update_appointment", methods=["PUT"])
def update_appointment():
    """
    Endpoint to update an existing appointment
    Get appointment details from customer and call db.update_appointment
    """
    new_visit_date = '2031-01-01'
    appointment_id = '12'
    try:
        db.update_appointment_db(con, new_visit_date, appointment_id), 200
        return {'message': f'Visit date has been changed to {new_visit_date}'}
    except psycopg2.DatabaseError:
        return {'message': 'Failed to update your appointment'}


@app.route("/cancel_appointment", methods=['DELETE'])
def cancel_appointment():
    """
    Endpoint to cancel an appointment
    Get appointment ID from customer and call db.remove_appointment
    """
    appointment_id = '7'
    try:
        db.cancel_appointment_db(con, appointment_id)
        return {'message': f'The appointment with appointment_id: {appointment_id} has been successfully '
                           f'deleted!'}, 200
    except psycopg2.DatabaseError:
        return {'message': 'Failed to cancel the appointment (appointment_id not exist)'}, 401


@app.route("/list_customer_appointments", methods=['GET'])
def list_customer_appointments():
    """
    Endpoint that returns appointments for a specific customer
    Get customer ID from customer and call db.view_appointments_for_customer
    """
    password = 'test'
    try:
        column_names, appointments = db.list_appointments_db(con, password)
        if not appointments:
            return {'message': 'Failed to retrieve all your appointments (Wrong Password)'}, 401
        else:
            return {'message': appointments}, 200
    except psycopg2.DatabaseError:
        return {'message': 'Failed to retrieve customer appointments'}, 400


@app.route("/favorite_listing", methods=['GET'])
def favorite_listing():
    """
    Endpoint to let a customer favorite a specific listing
    Should ideally only need a title, it's your choice how to implement it
    """
    password = 'test'
    liked_disliked = True
    try:
        column_names, liked_disliked_list = db.view_favorite_unfavorite_lists_db(con, password, liked_disliked)
        if not liked_disliked_list:
            return {'message': 'Failed to retrieve all your favorite lists (Wrong Password)'}, 401
        else:
            return {'message': liked_disliked_list}, 200
    except psycopg2.DatabaseError:
        return {'message': 'Failed to retrieve all your favorite lists'}, 400


@app.route("/unfavorite_listing", methods=['GET'])
def unfavorite_listing():
    """
    Endpoint to let a customer unfavorite a specific listing
    Should ideally only need a title, but it's your choice how to implement it
    """
    password = 'test'
    liked_disliked = False
    try:
        column_names, liked_disliked_list = db.view_favorite_unfavorite_lists_db(con, password, liked_disliked)
        if not liked_disliked_list:
            return {'message': 'Failed to retrieve all your unfavorite lists (Wrong Password)'}, 401
        else:
            return {'message': liked_disliked_list}, 200
    except psycopg2.DatabaseError:
        return {'message': 'Failed to retrieve all your unfavorite lists'}, 400