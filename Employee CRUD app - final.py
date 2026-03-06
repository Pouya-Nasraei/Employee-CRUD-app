import os
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Connection Error", f"Database connection failed:\n{e}")
        return None


def validate_id(emp_id):
    if not emp_id.isdigit():
        messagebox.showwarning("Validation Error", "Employee ID must be numeric.")
        return False
    return True


def insertData():
    emp_id = enterId.get().strip()
    name = enterName.get().strip()
    dept = enterDept.get().strip()

    if not emp_id or not name or not dept:
        messagebox.showwarning("Insert Error", "All fields are required!")
        return

    if not validate_id(emp_id):
        return

    db = get_connection()
    if not db:
        return

    try:
        cursor = db.cursor()
        query = "INSERT INTO empDetails (empId, empName, empDept) VALUES (%s, %s, %s)"
        cursor.execute(query, (emp_id, name, dept))
        db.commit()
        messagebox.showinfo("Success", "Employee added successfully!")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        db.close()
        resetfields()


def updateData():
    emp_id = enterId.get().strip()
    name = enterName.get().strip()
    dept = enterDept.get().strip()

    if not emp_id or not name or not dept:
        messagebox.showwarning("Update Error", "All fields are required!")
        return

    if not validate_id(emp_id):
        return

    db = get_connection()
    if not db:
        return

    try:
        cursor = db.cursor()
        query = "UPDATE empDetails SET empName=%s, empDept=%s WHERE empId=%s"
        cursor.execute(query, (name, dept, emp_id))
        db.commit()

        if cursor.rowcount == 0:
            messagebox.showinfo("Not Found", "No employee found with that ID.")
        else:
            messagebox.showinfo("Success", "Employee updated successfully!")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        db.close()
        resetfields()


def getData():
    emp_id = enterId.get().strip()

    if not emp_id:
        messagebox.showwarning("Fetch Error", "Enter an ID to fetch data.")
        return

    if not validate_id(emp_id):
        return

    db = get_connection()
    if not db:
        return

    try:
        cursor = db.cursor()
        query = "SELECT empName, empDept FROM empDetails WHERE empId=%s"
        cursor.execute(query, (emp_id,))
        row = cursor.fetchone()

        if row:
            resetfields()
            enterId.insert(0, emp_id)
            enterName.insert(0, row[0])
            enterDept.insert(0, row[1])
        else:
            messagebox.showinfo("Not Found", "No employee found with that ID.")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        db.close()


def deleteData():
    emp_id = enterId.get().strip()

    if not emp_id:
        messagebox.showwarning("Delete Error", "Enter an ID to delete.")
        return

    if not validate_id(emp_id):
        return

    db = get_connection()
    if not db:
        return

    try:
        cursor = db.cursor()
        query = "DELETE FROM empDetails WHERE empId=%s"
        cursor.execute(query, (emp_id,))
        db.commit()

        if cursor.rowcount == 0:
            messagebox.showinfo("Not Found", "No employee found with that ID.")
        else:
            messagebox.showinfo("Deleted", "Employee deleted successfully.")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        db.close()
        resetfields()


def show():
    db = get_connection()
    if not db:
        return

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM empDetails")
        rows = cursor.fetchall()

        showData.delete(0, tk.END)
        for row in rows:
            showData.insert(tk.END, f"{row[0]}  {row[1]}  {row[2]}")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        db.close()


def resetfields():
    enterId.delete(0, tk.END)
    enterName.delete(0, tk.END)
    enterDept.delete(0, tk.END)


window = tk.Tk()
window.geometry("550x350")
window.title("Employee CRUD App")

tk.Label(window, text="Employee ID:").place(x=20, y=30)
tk.Label(window, text="Employee Name:").place(x=20, y=70)
tk.Label(window, text="Employee Dept:").place(x=20, y=110)

enterId = tk.Entry(window, width=25)
enterId.place(x=170, y=30)

enterName = tk.Entry(window, width=25)
enterName.place(x=170, y=70)

enterDept = tk.Entry(window, width=25)
enterDept.place(x=170, y=110)

tk.Button(window, text="Insert", width=10, command=insertData).place(x=20, y=160)
tk.Button(window, text="Update", width=10, command=updateData).place(x=110, y=160)
tk.Button(window, text="Fetch", width=10, command=getData).place(x=200, y=160)
tk.Button(window, text="Delete", width=10, command=deleteData).place(x=290, y=160)
tk.Button(window, text="Reset", width=10, command=resetfields).place(x=150, y=210)
tk.Button(window, text="Show All", width=10, command=show).place(x=240, y=210)

showData = tk.Listbox(window, width=40)
showData.place(x=350, y=30)

window.mainloop()
