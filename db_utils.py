import sqlite3
from item import Item

def add_item(name):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    command = "INSERT INTO items(name,quantity) values(?,?)"
    values = (name, 1)
    cursor.execute(command,values)
    conn.commit()
    conn.close()

def generate_items():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    command = "SELECT * FROM items"
    cursor.execute(command)
    rows = cursor.fetchall()
    conn.close()
    items = []
    for row in rows:
        item = Item(row[0],row[1])
        items.append(item)
    return items

def increment_item(item):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET quantity = quantity+1 WHERE name = ?", (str(item.get_name()),))
    conn.commit()
    conn.close()


def decrement_item(item):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET quantity = quantity-1 WHERE name = ?", (str(item.get_name()),))
    conn.commit()
    conn.close()

def delete_item(item):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE name = ?", (str(item.get_name()),))
    conn.commit()
    conn.close()
