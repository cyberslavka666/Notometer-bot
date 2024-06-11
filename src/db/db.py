from psycopg2 import *

params = {
    "dbname": "not-bot",
    "user": "postgres",
    "password": "qwerty12345",
    "host": "127.0.0.1",
    "port": "5432"
}

connection = connect(**params)
cursor = connection.cursor()