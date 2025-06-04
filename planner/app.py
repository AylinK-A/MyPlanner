import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import threading
from datetime import datetime
from planner.core import init_db, add_task, delete_task_by_id, get_tasks, get_tasks_by_date, run_scheduler
from tkinter import ttk
from PIL import Image, ImageTk


def show_start_screen():
    start = tk.Tk()
    start.title("Добро пожаловать")
    start.attributes("-fullscreen", True)
    start.resizable(False, False)

    screen_width = start.winfo_screenwidth()
    screen_height = start.winfo_screenheight()

    
    bg_image = Image.open("assets/background.jpg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(start, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Надпись "ЛИЧНЫЙ ПЛАНЕР"
    tk.Label(start, text="ЛИЧНЫЙ ПЛАНЕР", font=("Helvetica", 40, "bold"),
             fg="white", bg="#4b2e83").place(relx=0.5, rely=0.3, anchor="center")

    # Кнопка
    def start_planner():
        start.destroy()
        run_app()

    tk.Button(start, text="ПРИСТУПИТЬ К ПЛАНИРОВАНИЮ", font=("Arial", 30),
              bg="#ff69b4", fg="black", activebackground="#ff85c1",
              command=start_planner).place(relx=0.5, rely=0.6, anchor="center")

    start.mainloop()


def run_app():
    def get_quote():
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "☀️ Доброе утро! Сегодня отличный день для новых задач."
        elif 12 <= hour < 17:
            return "🌤 Отличный день — не забудь сделать что-то важное."
        elif 17 <= hour < 22:
            return "🌇 Вечер — пора подвести итоги и немного отдохнуть."
        else:
            return "🌙 Спокойной ночи! Завтра снова будут новые цели."

    def refresh_tasks():
        for i in tree.get_children():
            tree.delete(i)
        for index, (tid, task, date, time_str) in enumerate(get_tasks()):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            tree.insert("", "end", iid=tid, values=(task, date, time_str), tags=(tag,))

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
        selected = tree.selection()
        if selected:
            task_id = selected[0]
            delete_task_by_id(task_id)
            refresh_tasks()
        else:
            messagebox.showwarning("Ошибка", "Выберите задачу")

    def show_for_date():
        selected_date = cal.get_date()
        tasks = get_tasks_by_date(selected_date)
        for i in tree.get_children():
            tree.delete(i)
        if tasks:
            for index, (task, date, time_str) in enumerate(tasks):
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=(f"  {task}", date, time_str), tags=(tag,))
        else:
            tree.insert("", "end", values=("Нет задач", "", ""))

    def on_double_click(event):
        selected = tree.selection()
        if selected:
            item_id = selected[0]
            values = tree.item(item_id, "values")
            task_text = values[0]
            if item_id not in completed_tasks:
                tree.item(item_id, values=(f"✅ {task_text.strip()}", values[1], values[2]))
                completed_tasks.add(item_id)
            else:
                tree.item(item_id, values=(task_text.replace("✅", "").strip(), values[1], values[2]))
                completed_tasks.remove(item_id)

    # === Окно ===
    app = tk.Tk()
    app.title("Планер")
    app.attributes("-fullscreen", True)

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # === Фон ===
    bg_image = Image.open("assets/background.jpg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(app, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # === Цвета ===
    background_color = "#fff0f5"
    panel_bg = "#ffffff"
    button_color = "#ff69b4"
    button_hover = "#ff85c1"
    title_color = "#4b2e83"

    # === Контейнер ===
    container = tk.Frame(app, bg=background_color)
    container.place(relx=0, rely=0, relwidth=1, relheight=1)

    # === Заголовок ===
    tk.Label(container, text="ЛИЧНЫЙ ПЛАНЕР", font=("Helvetica", 32, "bold"),
             fg=title_color, bg=background_color).pack(pady=(30, 10))

    # === Цитата ===
    tk.Label(container, text=get_quote(), font=("Helvetica", 16, "italic"),
             bg=background_color, fg="#555555").pack(pady=(0, 20))

    # === Основной фрейм ===
    main_frame = tk.Frame(container, bg=background_color)
    main_frame.pack(fill="both", expand=True, padx=60, pady=10)

    # === Левая панель ===
    left_panel = tk.Frame(main_frame, bg=panel_bg, bd=2, relief="groove")
    left_panel.pack(side="left", fill="y", padx=60, pady=60)

    tk.Label(left_panel, text="📅 Выберите дату", font=("Arial", 16), bg=panel_bg).pack(pady=20)

    cal = Calendar(left_panel, date_pattern='dd.mm.yyyy', font=("Arial", 14), selectmode='day',
               background="white", foreground="black", selectbackground=button_color,
               selectforeground="red", 
               headersbackground="lightgrey")
    
    cal.pack(pady=30, ipadx=30, ipady=20)


    tk.Label(left_panel, text="⏰ Время (чч:мм)", font=("Arial", 14), bg=panel_bg).pack(pady=(20, 5))
    time_entry = tk.Entry(left_panel, font=("Arial", 14), width=20)
    time_entry.pack(pady=(0, 20))

    # === Правая панель ===
    right_panel = tk.Frame(main_frame, bg=panel_bg, bd=2, relief="groove")
    right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    tk.Label(right_panel, text="✍️ Новая задача", font=("Arial", 16), bg=panel_bg).pack(pady=(20, 5))
    task_entry = tk.Entry(right_panel, font=("Arial", 14), width=60)
    task_entry.pack(pady=(0, 20), ipady=5)

    # === Кнопки ===
    btn_frame = tk.Frame(right_panel, bg=panel_bg)
    btn_frame.pack(pady=10)

    button_style = {"font": ("Arial", 12), "width": 15, "height": 3,
                    "bg": button_color, "fg": "black", "activebackground": button_hover}
    tk.Button(btn_frame, text="Добавить", command=add_task_gui, **button_style).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Удалить", command=delete_selected_task, **button_style).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="Планы на день", command=show_for_date, **button_style).grid(row=0, column=2, padx=10)

    separator = ttk.Separator(right_panel, orient='horizontal')
    separator.pack(fill='x', padx=10, pady=(10, 20))

    def on_enter(e):
        e.widget.config(bg="#ff85c1")

    def on_leave(e):
        e.widget.config(bg=button_color)

    for btn in btn_frame.winfo_children():
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # === Таблица задач ===
    tk.Label(right_panel, text="📋 Список задач", font=("Arial", 16, "bold"), bg=panel_bg).pack(pady=(10, 30))

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 14), rowheight=30,
                    background="white", fieldbackground="white", foreground="black")
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
    style.map("Treeview", background=[("selected", "#d1e7dd")])

    tree = ttk.Treeview(right_panel, columns=("task", "date", "time"), show="headings", height=15)
    tree.heading("task", text="Задача")
    tree.heading("date", text="Дата")
    tree.heading("time", text="Время")
    tree.column("task", width=450, anchor="w")
    tree.column("date", width=120, anchor="center")
    tree.column("time", width=100, anchor="center")
    tree.tag_configure("oddrow", background="#f9f9f9")
    tree.tag_configure("evenrow", background="#ffffff")
    tree.pack(pady=5)
    tree.bind("<Double-1>", on_double_click)

    completed_tasks = set()

    init_db()
    refresh_tasks()
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.mainloop()