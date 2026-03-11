import os
import mysql.connector
from dotenv import load_dotenv
import logging

load_dotenv()

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        logging.info("Database connection successful")
        return connection

    except mysql.connector.Error as e:
        logging.error(f"Database connection failed: {e}")
        return None