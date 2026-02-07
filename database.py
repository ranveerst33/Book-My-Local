import mysql.connector
from mysql.connector import Error

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  #Enter your mysql username
        password='YourPassword',  #Enter your mysql password
        database='train_ticket'
    )