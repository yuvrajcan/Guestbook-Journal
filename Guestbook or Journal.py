import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('guestbook.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        comment TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
''')
conn.commit()

# Function to add entry to the database
def add_entry():
    name = name_entry.get()
    comment = comment_entry.get("1.0", tk.END).strip()
    
    if name and comment:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('INSERT INTO entries (name, comment, timestamp) VALUES (?, ?, ?)', (name, comment, timestamp))
        conn.commit()
        name_entry.delete(0, tk.END)
        comment_entry.delete("1.0", tk.END)
        load_entries()
    else:
        messagebox.showwarning("Input Error", "Name and comment cannot be empty!")

# Function to load entries from the database
def load_entries():
    entries_list.delete(0, tk.END)
    c.execute('SELECT * FROM entries ORDER BY timestamp DESC')
    rows = c.fetchall()
    for row in rows:
        entries_list.insert(tk.END, f"{row[1]} ({row[3]}):\n{row[2]}\n")

# GUI setup
root = tk.Tk()
root.title("Guestbook / Journal")

# Name Entry
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(root, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=10)

# Comment Entry
tk.Label(root, text="Comment:").grid(row=1, column=0, padx=10, pady=10)
comment_entry = tk.Text(root, width=40, height=10)
comment_entry.grid(row=1, column=1, padx=10, pady=10)

# Submit Button
submit_button = tk.Button(root, text="Add Entry", command=add_entry)
submit_button.grid(row=2, column=1, padx=10, pady=10, sticky=tk.E)

# Entries List
entries_list = tk.Listbox(root, width=80, height=20)
entries_list.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Load existing entries on startup
load_entries()

# Start the GUI loop
root.mainloop()

# Close the database connection when the application is closed
conn.close()
