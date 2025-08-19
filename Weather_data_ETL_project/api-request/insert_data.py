import psycopg2, os
from dotenv import load_dotenv
from api_request import extract_data

# Load .env file
load_dotenv()

# Read credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def connect_to_db():
    print("Connecting to the PostgreSQL database...")
    try:
        conn = psycopg2.connect(
            host= DB_HOST,
            port= DB_PORT,
            dbname= DB_NAME,
            user= DB_USER,
            password= DB_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data(
                       id SERIAL PRIMARY KEY,
                       city TEXT,
                       temperature FLOAT,
                       weather_descriptions TEXT,
                       wind_speed FLOAT,
                       time TIMESTAMP,
                       inserted_at TIMESTAMP DEFAULT NOW(),
                       ufc_offset TEXT
            );
    """)
        conn.commit()
        print("Table was created")
    except psycopg2.Error as e:
        print(f"Failed to create a table: {e}")
        raise

def insert_data(conn, data):
    location = data['location']
    weather = data['current']
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dev.raw_weather_data(
                city,
                temperature,
                weather_descriptions,
                wind_speed,
                time,
                inserted_at,
                ufc_offset
            ) VALUES(%s, %s, %s, %s, %s, NOW(), %s)
        """,(
            location['name'],
            weather['temperature'],
            weather['weather_descriptions'][0],
            weather['wind_speed'],
            location['localtime'],
            location['utc_offset']
        ))
        conn.commit()
        print("Data is inserted successfully")
    
    except psycopg2.Error as e:
        print(f"Error inserting data to the DB: {e}")
        raise

def main():
    try:
        data = extract_data()
        conn = connect_to_db()
        create_table(conn)
        insert_data(conn,data)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

# main()

