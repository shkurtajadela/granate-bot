from dotenv import load_dotenv
import os
import psycopg2

load_dotenv('.env')
password = os.getenv("PASSWORD")


def create_tables():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password=password,
        port='5432'
    )

    # Create a cursor object
    cur = conn.cursor()

    # Define SQL statements to create tables
    create_question_table = '''
        CREATE TABLE IF NOT EXISTS question (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            question TEXT NOT NULL,
            answered BOOLEAN NOT NULL DEFAULT FALSE
        )
    '''

    create_notification_table = '''
        CREATE TABLE IF NOT EXISTS notification (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            get_notified BOOLEAN NOT NULL DEFAULT FALSE
        )
    '''

    create_user_table = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            admin BOOLEAN NOT NULL DEFAULT FALSE
        )
    '''

    # Execute the SQL statements
    cur.execute(create_question_table)
    cur.execute(create_notification_table)
    cur.execute(create_user_table)

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

# Run the create_tables function
create_tables()
