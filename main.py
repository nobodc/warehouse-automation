import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def save_data():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory
                      (id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER, category TEXT, sku TEXT, sold INTEGER)''')

    for row_entries in entries:
        values = []
        skip_row = False
        for entry in row_entries[1:]:
            if isinstance(entry, ttk.Combobox):
                value = entry.get()
            else:
                value = entry.get()

            if value == "":
                skip_row = True
                break
            values.append(value)

        if not skip_row:
            cursor.execute(
                'INSERT INTO inventory (name, price, quantity, category, sku, sold) VALUES (?, ?, ?, ?, ?, ?)', values)

    conn.commit()
    conn.close()
    messagebox.showinfo("Успех", "Данные сохранены успешно!")


def clear_inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM inventory')
    conn.commit()
    conn.close()
    messagebox.showinfo("Успех", "Инвентарь очищен успешно!")


def show_inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    rows = cursor.fetchall()
    conn.close()

    total_quantity = sum(row[3] for row in rows)

    if not rows:
        messagebox.showinfo("Инвентарь", "Инвентарь пуст!")
    else:
        inventory_data = f"Общее кол-во товаров: {total_quantity}\n\n"
        for row in rows:
            inventory_data += f"{row[1]} | Цена: {row[2]} руб. | Осталось: {row[3]}шт | {row[4]} |\nАртикул: {row[5]} | Продано: {row[6]}шт\n\n"
        messagebox.showinfo("Инвентарь", inventory_data)
root = tk.Tk()
root.title("Управление складом")
root.geometry("1100x500")


headers = ["№", "Наименование товара", "Цена товара", "Количество товаров", "Вид товаров", "Артикул", "Продано"]
for i, header in enumerate(headers):
    tk.Label(root, text=header,font=("Arial", 13)).grid(row=0, column=i)

entries = []
for i in range(1, 7):
    row_entries = []
    for j in range(len(headers)):
        if j == 0:
            entry = tk.Label(root, text=str(i),font=("Arial", 13))
            entry.grid(row=i, column=j)
        elif j == 4:
            entry = ttk.Combobox(root, values=["Одежда/Обувь", "Продукты", "Электронника", "Бытовая техника", "Ремонт"], font=("Arial", 13))
            entry.grid(row=i, column=j)
        else:
            entry = tk.Entry(root, font=("Arial", 13))
            entry.grid(row=i, column=j)
        row_entries.append(entry)
    entries.append(row_entries)



save_button = tk.Button(root, text=" Сохранить данные ", font=("Arial", 13), command=save_data)
save_button.grid(row=8, column=3, pady=(13,0))

show_inventory = tk.Button(root, text="Показать инвентарь", font=("Arial", 13), command=show_inventory)
show_inventory.grid(row=9, column=3)

load_button = tk.Button(root, text="Очистить инвентарь", font=("Arial", 13), command=clear_inventory)
load_button.grid(row=10, column=3)

root.mainloop()

