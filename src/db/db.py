from psycopg2 import *

params = {
    "dbname": "your-db-name",
    "user": "your-user",
    "password": "your-password",
    "host": "127.0.0.1",
    "port": "5432"
}

connection = connect(**params)
cursor = connection.cursor()
