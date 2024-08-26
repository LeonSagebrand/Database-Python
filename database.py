"""This file is responsible for doing CRUD and make queries in backend and send them to frontend"""
import psycopg2 as pg
from dotenv import load_dotenv
import os



load_dotenv()

DATABASE_NAME = os.getenv("database_lab2")
pw = os.getenv("postgres")

# Optional, add these to psycopg.connect() if you need to
DATABASE_PORT = os.getenv("5432")  # default is normally 5432
DATABASE_USER = os.getenv("postgres")  # default is normally postgres


def connect_db(pw):
    """Establishes a connection to the database."""
    try:
        conn = pg.connect(dbname="database_lab2", password=pw, user="postgres", port=5432)
        return conn
    except pg.DatabaseError as e:
        print(f"Database connection failed: {e}")
        raise


con = connect_db(pw)
# -----------------------------------------Admin Functions------------------------------------------------------------ #


def execution(con, query_name, args=()):
    with con:
        with con.cursor() as cursor:
            cursor.execute(query_name, args)
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return column_names, result


def create_tables(con):
    create_users_table_query = """
        CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY,
            first_name VARCHAR(200) NOT NULL,
            last_name VARCHAR(200) NOT NULL,
            phone_number VARCHAR(30) UNIQUE NOT NULL,
            email VARCHAR(500) UNIQUE NOT NULL,
            password VARCHAR(250) UNIQUE NOT NULL,
            admin BOOLEAN default false
    )
    """

    create_categories_table_query = """
        CREATE TABLE IF NOT EXISTS categories(
            type_id SERIAL PRIMARY KEY,
            type_name VARCHAR(200)
    )
    """

    create_counties_table_query = """
        CREATE TABLE IF NOT EXISTS counties(
            county_id SERIAL PRIMARY KEY,
            county_name VARCHAR(200)
    )
    """

    create_municipalities_table_query = """
        CREATE TABLE IF NOT EXISTS municipalities(
            municipality_id SERIAL PRIMARY KEY,
            municipality_name VARCHAR(200),
            county_id INT REFERENCES counties(county_id)
    )
    """

    create_brokers_table_query = """
        CREATE TABLE IF NOT EXISTS brokers(
            broker_id SERIAL PRIMARY KEY,
            first_name VARCHAR(200) NOT NULL,
            last_name VARCHAR(200) NOT NULL,
            phone_number VARCHAR UNIQUE NOT NULL
    )
    """

    create_lists_table_query = """
            CREATE TABLE IF NOT EXISTS lists(
                list_id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(user_id),
                broker_id INT REFERENCES brokers(broker_id),
                type_id INT REFERENCES categories(type_id),
                municipality_id INT REFERENCES municipalities(municipality_id),
                address VARCHAR(500) NOT NULL,
                postal_code VARCHAR(10) NOT NULL,
                size SMALLINT NOT NULL,
                number_of_rooms SMALLINT NOT NULL,
                year_of_construction VARCHAR(4),
                description TEXT,
                price NUMERIC(20, 2) NOT NULL,
                date_announced DATE DEFAULT current_date,
                balcony VARCHAR(3),
                elevator VARCHAR(3)
        )
        """

    create_favorite_list_table_query = """
        CREATE TABLE IF NOT EXISTS wish_list(
            wish_list_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id),
            list_id INT REFERENCES lists(list_id),
            liked BOOLEAN NOT NULL,
            UNIQUE (user_id, list_id)
    )
    """

    create_appointments_table_query = """
        CREATE TABLE IF NOT EXISTS appointments(
            appointment_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id),
            broker_id INT REFERENCES brokers(broker_id),
            visit_date DATE
    )
    """

    add_brokers_query = """
        INSERT INTO brokers(first_name, last_name, phone_number)
        VALUES 
        ('Kamjar', 'Shahi', '709997931'),
        ('Victoria', 'Knaller', '725033239'),
        ('David', 'Strand', '709634183'),
        ('Victor', 'Gustafsson', '730653922'),
        ('Peter', 'Ablahad', '739201713'),
        ('Emmi', 'Englund', '708783708'),
        ('Tobias', 'Bemarre', '739545788'),
        ('Valencia', 'Can', '707103966'),
        ('Rebecca', 'Jansson', '709287436'),
        ('Nina', 'Ekberg', '709594545')
    """

    add_counties_query = """
            INSERT INTO counties(county_name)
            VALUES 
            ('Dalarna län'),
            ('Kalmar län'),
            ('Stockholm län'),
            ('Uppsala län'),
            ('Örebro län')
        """

    add_municipalities_query = """
            INSERT INTO municipalities(municipality_name, county_id)
            VALUES 
            ('Avesta', (SELECT county_id FROM counties WHERE county_name = 'Dalarna län')),
            ('Borlänge', (SELECT county_id FROM counties WHERE county_name = 'Dalarna län')),
            ('Borgholms', (SELECT county_id FROM counties WHERE county_name = 'Kalmar län')),
            ('Emmaboda', (SELECT county_id FROM counties WHERE county_name = 'Kalmar län')),
            ('Botkyrka', (SELECT county_id FROM counties WHERE county_name = 'Stockholm län')),
            ('Danderyds', (SELECT county_id FROM counties WHERE county_name = 'Stockholm län')),
            ('Enköpings', (SELECT county_id FROM counties WHERE county_name = 'Uppsala län')),
            ('Heby', (SELECT county_id FROM counties WHERE county_name = 'Uppsala län')),
            ('Askersunds', (SELECT county_id FROM counties WHERE county_name = 'Örebro län')),
            ('Degerfors', (SELECT county_id FROM counties WHERE county_name = 'Örebro län'))
        """
    add_categories_query = """
            INSERT INTO categories(type_name)
            VALUES 
            ('Apartments'),
            ('Villas'),
            ('House'),
            ('Leisure House'),
            ('Farms')
        """

    with con:
        with con.cursor() as cursor:
            cursor.execute(create_users_table_query)
            cursor.execute(create_categories_table_query)
            cursor.execute(create_counties_table_query)
            cursor.execute(create_municipalities_table_query)
            cursor.execute(create_brokers_table_query)
            cursor.execute(create_lists_table_query)
            cursor.execute(create_favorite_list_table_query)
            cursor.execute(create_appointments_table_query)
            cursor.execute(add_brokers_query)
            cursor.execute(add_counties_query)
            cursor.execute(add_municipalities_query)
            cursor.execute(add_categories_query)


def add_users_db(con, first_name, last_name, phone_number, email, password, admin):
    add_users_query = """
        INSERT INTO users(first_name, last_name, phone_number, email, password, admin)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    with con:
        with con.cursor() as cursor:
            cursor.execute(add_users_query, (first_name, last_name, phone_number, email, password, admin))


def delete_list_admin_db(con, list_id):
    delete_list_admin_query = """
        DELETE FROM lists USING users
        WHERE list_id = %s AND users.admin = true
        RETURNING *;
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(delete_list_admin_query, (list_id, ))
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchone()


def list_lists_db(con):
    """admin viewing lists"""
    list_lists_query = """
        SELECT * FROM lists
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(list_lists_query)
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchall()


def list_category_db(con):
    list_category_query = """
            SELECT * FROM categories
        """
    with con:
        with con.cursor() as cursor:
            cursor.execute(list_category_query)
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchall()


def add_category_db(con, type_name):
    add_category_query = """
        INSERT INTO categories(type_name)
        VALUES (%s)
    """

    with con:
        with con.cursor() as cursor:
            cursor.execute(add_category_query, (type_name, ))


def update_category_db(con, new_type_name, type_id):
    update_category_query = '''
        UPDATE categories
        SET type_name = %s
        WHERE type_id = %s
        RETURNING *;
'''
    with con:
        with con.cursor() as cursor:
            cursor.execute(update_category_query, (new_type_name, type_id))
            broker_id = cursor.fetchone()[0]
            return broker_id


def list_users_db(con):
    list_users_query = """
        SELECT * FROM users
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(list_users_query)
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchall()


def list_brokers_db(con):
    list_brokers_query = """
        SELECT * FROM brokers
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(list_brokers_query)
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchall()

# -----------------------------------------Users Functions------------------------------------------------------------ #


def delete_user_profile_db(con, password):
    delete_user_profile_query = '''
            DELETE FROM users
            WHERE password = %s
            RETURNING *;
    '''
    with con:
        with con.cursor() as cursor:
            cursor.execute(delete_user_profile_query, (password,))
            user_id = cursor.fetchone()[0]
            return user_id


def check_password_db(con, password):
    check_password_query = """
        SELECT password FROM users
        WHERE password = %s;
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(check_password_query, (password,))
            user_id = cursor.fetchone()[0]
            return user_id


def add_listing_db(con, password, broker_id, category, municipality, address, postal_code, size, number_of_rooms,
                   year_of_construction, description, price, balcony, elevator):
    add_listing_query = """
    INSERT INTO lists(user_id, broker_id, type_id, municipality_id, address, postal_code, size, number_of_rooms,
    year_of_construction, description, price, balcony, elevator)
    VALUES 
    ((SELECT user_id FROM users WHERE password = %s), (SELECT broker_id FROM brokers WHERE broker_id = %s),
    (SELECT type_id FROM categories WHERE type_name ILIKE %s),
    (SELECT municipality_id FROM municipalities WHERE municipality_name ILIKE %s), %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    with con:
        with con.cursor() as cursor:
            cursor.execute(add_listing_query, (password, broker_id, category, municipality, address, postal_code, size, number_of_rooms,
                                               year_of_construction, description, price, balcony, elevator))


def delete_list_user_db(con, list_id, password):
    delete_list_user_query = """
        DELETE FROM lists USING users
        WHERE list_id = %s AND users.password = %s
        RETURNING *;
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(delete_list_user_query, (list_id, password))
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchone()


def choosing_broker_db(con):
    choosing_broker_query = """
        SELECT * FROM brokers
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(choosing_broker_query)
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchall()


def user_lists_db(con, password):
    """users viewing lists"""
    list_lists_query = """
        SELECT list_id, broker_id, postal_code, size, number_of_rooms, year_of_construction, price, date_announced FROM lists
        INNER JOIN users ON lists.user_id = users.user_id
        WHERE password = %s;
    """
    column_names, result = execution(con=con, query_name=list_lists_query, args=(password,))
    return column_names, result


def add_favorite_unfavorites_lists_db(con, password, list_id, like_dislike):
    favorite_unfavorites_lists_query = """
        INSERT INTO wish_list (user_id, list_id, liked)
        VALUES ((SELECT user_id FROM users WHERE password = %s), %s, %s)
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(favorite_unfavorites_lists_query, (password, list_id, like_dislike))


def view_favorite_unfavorite_lists_db(con, password, liked_disliked):
    view_favorite_unfavorite_lists_query = """
    SELECT lists.list_id, liked, municipality_id, address, postal_code, size, number_of_rooms, price, description, year_of_construction, balcony, elevator FROM wish_list
    INNER JOIN lists ON wish_list.list_id = lists.list_id
    INNER JOIN users ON users.user_id = wish_list.user_id
    WHERE password = %s AND liked = %s;
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(view_favorite_unfavorite_lists_query, (password, liked_disliked))
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchall()


def book_appointment_db(con, password, broker_id, visit_date):
    book_appointment_query = """
        INSERT INTO appointments(user_id, broker_id, visit_date)
        VALUES ((SELECT user_id FROM users WHERE password = %s), (SELECT broker_id FROM lists WHERE lists.list_id = %s),
        %s)
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(book_appointment_query, (password, broker_id, visit_date))


def list_appointments_db(con, password):
    list_appointments_query = """
        SELECT * FROM appointments
        INNER JOIN users ON appointments.user_id = users.user_id
        WHERE password = %s
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(list_appointments_query, (password, ))
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchall()


def cancel_appointment_db(con, appointment_id):
    cancel_appointment_query = """
        DELETE FROM appointments
        WHERE appointment_id = %s
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(cancel_appointment_query, (appointment_id,))


def view_appointments_user_db(con, password):
    view_appointments_user_query = """
        SELECT appointment_id, brokers.first_name, brokers.last_name, brokers.phone_number, visit_date FROM appointments
        INNER JOIN users ON appointments.user_id = users.user_id
        INNER JOIN brokers ON appointments.broker_id = brokers.broker_id
        WHERE users.password = %s;
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(view_appointments_user_query, (password, ))
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchall()


def update_appointment_db(con, new_visit_date, appointment_id):
    update_appointment_query = """
        UPDATE appointments
        SET visit_date = %s
        WHERE appointment_id = %s
        RETURNING *;
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(update_appointment_query, (new_visit_date, appointment_id))
            appointment_id = cursor.fetchone()[0]
            return appointment_id


def update_user_profile_db(con, new_password, password):
    update_user_query = '''
        UPDATE users
        SET password = %s
        WHERE password = %s
        RETURNING *;
'''
    with con:
        with con.cursor() as cursor:
            cursor.execute(update_user_query, (new_password, password))
            user_id = cursor.fetchone()[0]
            return user_id


# -----------------------------------------Brokers Functions---------------------------------------------------------- #


def add_brokers_db(con, first_name, last_name, phone_number):
    add_brokers_query = """
        INSERT INTO brokers(first_name, last_name, phone_number)
        VALUES (%s, %s, %s) RETURNING broker_id
    """

    with con:
        with con.cursor() as cursor:
            cursor.execute(add_brokers_query, (first_name, last_name, phone_number))
            broker_id = cursor.fetchone()[0]
            return broker_id


def update_broker_profile_db(con, new_phone_number, phone_number):
    update_broker_query = """
        UPDATE brokers
        SET phone_number = %s
        WHERE phone_number = %s
        RETURNING *;
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(update_broker_query, (new_phone_number, phone_number))
            broker_id = cursor.fetchone()[0]
            return broker_id


def delete_broker_profile_db(con, phone_number):
    delete_broker_query = '''
        DELETE FROM brokers
        WHERE phone_number = %s
        RETURNING *;
'''
    with con:
        with con.cursor() as cursor:
            cursor.execute(delete_broker_query, (phone_number, ))
            broker_id = cursor.fetchone()[0]
            return broker_id


def view_appointments_broker_db(con, phone_number):
    view_appointments_broker_query = """
        SELECT users.first_name, users.last_name, users.phone_number, visit_date FROM appointments
        INNER JOIN users ON appointments.user_id = users.user_id
        INNER JOIN brokers ON appointments.broker_id = brokers.broker_id
        WHERE brokers.phone_number = %s;
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(view_appointments_broker_query, (phone_number, ))
            column_names = [desc[0] for desc in cursor.description]
            return column_names, cursor.fetchall()