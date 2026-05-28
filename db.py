import mysql.connector


def connect_db():

    try:

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="angel_cuala15",
            database="census"
        )

        print("Connected to database successfully!")

        return conn

    except mysql.connector.Error as err:

        print("DATABASE ERROR:")
        print(err)

        return None