import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import threading
from core import init_db, add_task, delete_task_by_id, get_tasks, get_tasks_by_date, run_scheduler


def run_app():
    def refresh_tasks():
        task_listbox.delete(0, tk.END)
        for tid, task, date, time_str in get_tasks():
            task_listbox.insert(tk.END, f"{tid} | {task} (Дата: {date}, Время: {time_str})")

    def add_task_gui():
        task = task_entry.get()
        date = cal.get_date()
        time_str = time_entry.get()
        if task and time_str:
            add_task(task, date, time_str)
            refresh_tasks()
            task_entry.delete(0, tk.END)
            time_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Введите задачу и время")

    def delete_selected_task():
        selected = task_listbox.curselection()
        if selected:
            task_id = task_listbox.get(selected[0]).split(" | ")[0]
            delete_task_by_id(task_id)
            refresh_tasks()
        else:
            messagebox.showwarning("Ошибка", "Выберите задачу")

    def show_for_date():
        selected_date = cal.get_date()
        tasks = get_tasks_by_date(selected_date)
        task_listbox.delete(0, tk.END)
        if tasks:
            for task, date, time_str in tasks:
                task_listbox.insert(tk.END, f"{task} (Дата: {date}, Время: {time_str})")
        else:
            task_listbox.insert(tk.END, "Нет задач")

    app = tk.Tk()
    app.title("Личный планер")
    app.geometry("600x700")
    app.configure(bg='#f0f0f0')
    app.resizable(False, False)

    # Поля ввода
    tk.Label(app, text="Задача", font=("Arial", 14), bg='#f0f0f0').pack()
    task_entry = tk.Entry(app, font=("Arial", 14))
    task_entry.pack(pady=5)

    tk.Label(app, text="Дата", font=("Arial", 14), bg='#f0f0f0').pack()
    cal = Calendar(app, date_pattern='dd.mm.yyyy')
    cal.pack(pady=5)

    tk.Label(app, text="Время (HH:MM)", font=("Arial", 14)).pack()
    time_entry = tk.Entry(app, font=("Arial", 14))
    time_entry.pack(pady=5)

    # Кнопки
    tk.Button(app, text="Добавить", command=add_task_gui, font=("Arial", 12), bg='lightgreen').pack(pady=5)
    tk.Button(app, text="Удалить", command=delete_selected_task, font=("Arial", 12), bg='salmon').pack(pady=5)
    tk.Button(app, text="Показать на день", command=show_for_date, font=("Arial", 12), bg='skyblue').pack(pady=5)

    # Список задач
    task_listbox = tk.Listbox(app, width=60, height=15, font=("Arial", 12))
    task_listbox.pack(pady=10)

    # Инициализация и запуск
    init_db()
    refresh_tasks()

    threading.Thread(target=run_scheduler, daemon=True).start()
    app.mainloop()

