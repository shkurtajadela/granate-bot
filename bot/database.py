import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv('.env')
password = os.getenv("PASSWORD")

def db_start():
    global conn, cur
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password=password,
        port='5432'
    )
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

    create_user_table = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            admin BOOLEAN NOT NULL DEFAULT FALSE,
            get_notified BOOLEAN NOT NULL DEFAULT FALSE
        )
    '''

    # Execute the SQL statements
    cur.execute(create_question_table)
    cur.execute(create_user_table)

    # Commit the changes
    conn.commit()


def db_close():
    global conn, cur
    cur.close()
    conn.close()

def add_question(chat_id: int, question: str):
    cur.execute("INSERT INTO question (chat_id, question) VALUES (%s, %s)", (chat_id, question,))
    conn.commit()
    cur.execute("SELECT id FROM question WHERE chat_id = %s and question = %s", (chat_id, question,))
    question_id = cur.fetchone()[0]
    return question_id

def add_user(chat_id: int):
    cur.execute("INSERT INTO users (chat_id) VALUES (%s)", (chat_id,))
    conn.commit()

def delete_user(chat_id: int):
    cur.execute("DELETE FROM users WHERE chat_id = %s", (chat_id,))
    conn.commit()

def update_users(chat_id: int):
    cur.execute("UPDATE users SET get_notified = true WHERE chat_id = %s", (chat_id,))
    conn.commit()

def update_question(chat_id: int, question_id: int):
    cur.execute("UPDATE question SET answered = true WHERE chat_id = %s and id = %s", (chat_id, question_id, ))
    conn.commit()

def find_question(chat_id: int, question_id: int):
    cur.execute("SELECT answered FROM question SET WHERE chat_id = %s and id = %s", (chat_id, question_id, ))
    try:
        question = cur.fetchone()[0]
        return True
    except:
        return False


def get_users():
    cur.execute("SELECT chat_id FROM users")
    users = cur.fetchall()
    numbers = [user[0] for user in users]
    return numbers

def get_users_notified():
    cur.execute("SELECT chat_id FROM users WHERE get_notified = true")
    users = cur.fetchall()
    numbers = [user[0] for user in users]
    return numbers

def get_admin():
    cur.execute("SELECT chat_id FROM users WHERE admin = true")
    users = cur.fetchall()
    numbers = [user[0] for user in users]
    return numbers