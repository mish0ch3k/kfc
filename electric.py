import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import unittest

CONFIG = {
    "DAY_TARIFF": 1.5,  
    "NIGHT_TARIFF": 0.9,  
    "EXTRA_DAY_KWH": 100,
    "EXTRA_NIGHT_KWH": 80
}

db_file = "meter_data.db"
test_db_file = "test_meter_data.db"

def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meter_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meter_id TEXT,
            date TEXT,
            previous_day REAL,
            previous_night REAL,
            day_usage REAL,
            night_usage REAL,
            cost REAL
        )
    ''')
    conn.commit()
    conn.close()

def init_test_db():
    conn = sqlite3.connect(test_db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meter_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meter_id TEXT,
            date TEXT,
            previous_day REAL,
            previous_night REAL,
            day_usage REAL,
            night_usage REAL,
            cost REAL
        )
    ''')
    conn.commit()
    conn.close()

def clear_test_db():
    conn = sqlite3.connect(test_db_file)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM meter_readings''')
    conn.commit()
    conn.close()

def save_reading_for_test(meter_id, day_kwh, night_kwh):
    if day_kwh < 0 or night_kwh < 0:
        return None
    
    prev_day, prev_night = get_last_reading(meter_id)
    
    if day_kwh < prev_day:
        day_kwh = prev_day + CONFIG["EXTRA_DAY_KWH"]
    if night_kwh < prev_night:
        night_kwh = prev_night + CONFIG["EXTRA_NIGHT_KWH"]
    
    day_usage = day_kwh - prev_day if day_kwh >= prev_day else CONFIG["EXTRA_DAY_KWH"]
    night_usage = night_kwh - prev_night if night_kwh >= prev_night else CONFIG["EXTRA_NIGHT_KWH"]
    
    cost = day_usage * CONFIG["DAY_TARIFF"] + night_usage * CONFIG["NIGHT_TARIFF"]
    
    conn = sqlite3.connect(test_db_file)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO meter_readings (meter_id, date, previous_day, previous_night, day_usage, night_usage, cost)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (meter_id, datetime.now().isoformat(), day_kwh, night_kwh, day_usage, night_usage, cost))
    conn.commit()
    conn.close()
    
    return cost

def get_last_reading(meter_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''SELECT previous_day, previous_night FROM meter_readings WHERE meter_id=? ORDER BY id DESC LIMIT 1''', (meter_id,))
    row = cursor.fetchone()
    conn.close()
    return row if row else (0, 0)

def get_meter_history(meter_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''SELECT date, day_usage, night_usage, cost FROM meter_readings WHERE meter_id=? ORDER BY id DESC''', (meter_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_reading(meter_id, day_kwh, night_kwh):
    if day_kwh < 0 or night_kwh < 0:
        messagebox.showerror("Помилка", "Показники не можуть бути від'ємними.")
        return None
    
    prev_day, prev_night = get_last_reading(meter_id)
    
    if day_kwh < prev_day:
        day_kwh = prev_day + CONFIG["EXTRA_DAY_KWH"]
    if night_kwh < prev_night:
        night_kwh = prev_night + CONFIG["EXTRA_NIGHT_KWH"]
    
    day_usage = day_kwh - prev_day if day_kwh >= prev_day else CONFIG["EXTRA_DAY_KWH"]
    night_usage = night_kwh - prev_night if night_kwh >= prev_night else CONFIG["EXTRA_NIGHT_KWH"]
    
    cost = day_usage * CONFIG["DAY_TARIFF"] + night_usage * CONFIG["NIGHT_TARIFF"]
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO meter_readings (meter_id, date, previous_day, previous_night, day_usage, night_usage, cost)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (meter_id, datetime.now().isoformat(), day_kwh, night_kwh, day_usage, night_usage, cost))
    conn.commit()
    conn.close()
    
    return cost

def submit_data():
    meter_id = entry_meter_id.get().strip()
    if not meter_id:
        messagebox.showerror("Помилка", "ID лічильника не може бути порожнім.")
        return
    
    try:
        day_kwh = float(entry_day_kwh.get())
        night_kwh = float(entry_night_kwh.get())
        cost = save_reading(meter_id, day_kwh, night_kwh)
        if cost is not None:
            messagebox.showinfo("Результат", f"Рахунок: {cost:.2f} грн")
            update_history(meter_id)
    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть коректні числові значення.")

def update_history(meter_id):
    for row in tree.get_children():
        tree.delete(row)
    history = get_meter_history(meter_id)
    for record in history:
        tree.insert("", "end", values=record)

def clear_entries():
    entry_meter_id.delete(0, tk.END)
    entry_day_kwh.delete(0, tk.END)
    entry_night_kwh.delete(0, tk.END)

# Тести
class TestMeterReading(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_test_db()

    @classmethod
    def tearDownClass(cls):
        clear_test_db()

    def setUp(self):
        clear_test_db()

    def test_update_existing_meter(self):
        meter_id = "meter1"
        save_reading_for_test(meter_id, 100, 50)
        result = save_reading_for_test(meter_id, 150, 80)
        self.assertIsNotNone(result, "Оновлення показників не вдалося")

    def test_new_meter(self):
        meter_id = "meter2"
        result = save_reading_for_test(meter_id, 120, 60)
        self.assertIsNotNone(result, "Не вдалося зберегти показники для нового лічильника")

    def test_lower_night_usage(self):
        meter_id = "meter3"
        save_reading_for_test(meter_id, 100, 50)
        result = save_reading_for_test(meter_id, 130, 40)
        self.assertIsNotNone(result, "Оновлення з заниженими нічними показниками не вдалося")

    def test_lower_day_usage(self):
        meter_id = "meter4"
        save_reading_for_test(meter_id, 100, 50)
        result = save_reading_for_test(meter_id, 90, 70)
        self.assertIsNotNone(result, "Оновлення з заниженими денними показниками не вдалося")

    def test_lower_day_and_night_usage(self):
        meter_id = "meter5"
        save_reading_for_test(meter_id, 100, 50)
        result = save_reading_for_test(meter_id, 80, 40)
        self.assertIsNotNone(result, "Оновлення з заниженими денними та нічними показниками не вдалося")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    root.title("Електролічильник")

    frame_inputs = tk.Frame(root)
    frame_inputs.pack(pady=10)

    tk.Label(frame_inputs, text="ID лічильника:").grid(row=0, column=0)
    entry_meter_id = tk.Entry(frame_inputs)
    entry_meter_id.grid(row=0, column=1)

    tk.Label(frame_inputs, text="Денні показники (кВт):").grid(row=1, column=0)
    entry_day_kwh = tk.Entry(frame_inputs)
    entry_day_kwh.grid(row=1, column=1)

    tk.Label(frame_inputs, text="Нічні показники (кВт):").grid(row=2, column=0)
    entry_night_kwh = tk.Entry(frame_inputs)
    entry_night_kwh.grid(row=2, column=1)

    tk.Button(frame_inputs, text="Розрахувати", command=submit_data).grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(frame_inputs, text="Очистити", command=clear_entries).grid(row=4, column=0, columnspan=2, pady=5)

    frame_history = tk.Frame(root)
    frame_history.pack(pady=10)

    tree = ttk.Treeview(frame_history, columns=("Дата", "День (кВт)", "Ніч (кВт)", "Вартість"), show="headings")
    for col in ("Дата", "День (кВт)", "Ніч (кВт)", "Вартість"):
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack()

    # Запуск тестів
    unittest.main(argv=[''], exit=False)

    root.mainloop()
