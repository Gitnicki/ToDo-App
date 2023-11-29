# Python Script to interact with the MySQL database
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values

# load_dotenv()
config = dotenv_values(".env")

# Serverconnection herstellen
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

def add_notes(todoitem, category):
    cursor = db_connection.cursor()
    sql = "INSERT INTO tasks (todoitem, category) VALUES (%s, %s)"
    val = (todoitem, category)
    cursor.execute(sql, val)
    db_connection.commit()
    print("Task added successfully!")

def view_tasks():
    cursor = db_connection.cursor()
    sql = "SELECT * FROM tasks"
    cursor.execute(sql)
    tasks = cursor.fetchall()
    if (tasks):
        for task in tasks:
            print(f"Task ID: {task[0]}, Task Name: {task[1]}, Description: {task[2]}, Status: {'Open' if task[3] else 'Finished'}")
    else:
        print("No Tasks in the DataBase")  


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