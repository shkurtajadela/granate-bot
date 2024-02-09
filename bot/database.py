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

def add_notification(chat_id: int):
    cur.execute("INSERT INTO notification (chat_id) VALUES (%s)", (chat_id, ))
    conn.commit()

def update_notification(chat_id: int):
    cur.execute("UPDATE notification SET get_notified = true WHERE chat_id = %s", (chat_id,))
    conn.commit()

def update_question(chat_id: int, question_id: int):
    cur.execute("UPDATE question SET answered = true WHERE chat_id = %s and id = %s", (chat_id, question_id, ))
    conn.commit()


def get_users():
    cur.execute("SELECT chat_id FROM users")
    users = cur.fetchall()
    numbers = [user[0] for user in users]
    return numbers

def get_users_notified():
    cur.execute("SELECT chat_id FROM notification WHERE get_notified = true")
    users = cur.fetchall()
    numbers = [user[0] for user in users]
    return numbers

def get_admin():
    cur.execute("SELECT chat_id FROM users WHERE admin = true")
    users = cur.fetchall()
    numbers = [user[0] for user in users]
    return numbers