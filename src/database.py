# Python Script to interact with the MySQL database
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values

# load_dotenv()

config = dotenv_values(".env")


def create_server_connection():
    connection = None
    host_name = config.get("DB_HOST")
    user_name = config.get("DB_USER")
    user_password = config.get("DB_PASSWORD")
    db_name = config.get("DB_NAME")
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password, database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def select_data(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")
        return None


def insert_data(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Data inserted successfully")
    except Error as err:
        print(f"Error: '{err}'")

def updateNotes(connection, id, todoitem, itemstatus, category):
    cursor = connection.cursor()
    query = "INSERT INTO notes (id, todoitem, itemstatus, category) VALUES (%s, %s, %s)"
    data = (id, todoitem, itemstatus, category)
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Data inserted successfully")
    except Error as err:
        print(f"Error: '{err}'")


# Establish a database connection
db_connection = create_server_connection()

# Sample usage of insert_data function
# insert_query = "INSERT INTO users (todoitem, itemstatus,category) VALUES (%s, %s, %s);"
# data_to_insert = ("Fritz", "Fischer", "fritz@fischer.de")
# insert_data(db_connection, insert_query, data_to_insert)

# Sample usage of select_data function
# select_query = "SELECT * FROM users;"
# selection_result = select_data(db_connection, select_query)
# print(selection_result)

db_connection.close()