import sqlite3
from datetime import datetime, timedelta
import schedule
import time

DB_NAME = 'planner.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_task(task, date, time):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task, date, time) VALUES (?, ?, ?)', (task, date, time))
    conn.commit()
    conn.close()
    schedule_task(task, date, time)

def delete_task_by_id(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, task, date, time FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_tasks_by_date(date_str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT task, date, time FROM tasks WHERE date = ?', (date_str,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def schedule_task(task, date, time_str):
    dt = datetime.strptime(f"{date} {time_str}", "%d.%m.%Y %H:%M")
    reminder = dt - timedelta(minutes=10)
    schedule.every().day.at(reminder.strftime("%H:%M")).do(lambda: print(f"🔔 Напоминание: {task}"))

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
