from tkinter import *
from tkinter import messagebox
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="NikePumaJ23*",
        database="employee"
    )

def insertData():
    emp_id = enterId.get()
    name = enterName.get()
    dept = enterDept.get()

    if not emp_id or not name or not dept:
        messagebox.showwarning("Insert Error", "All fields are required!")
        return

    try:
        db = get_connection()
        cursor = db.cursor()

        query = "INSERT INTO empDetails (empId, empName, empDept) VALUES (%s, %s, %s)"
        values = (emp_id, name, dept)

        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "Employee added successfully!")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        db.close()
        resetfields()


def updateData():
    emp_id = enterId.get()
    name = enterName.get()
    dept = enterDept.get()

    if not emp_id or not name or not dept:
        messagebox.showwarning("Update Error", "All fields are required!")
        return

    try:
        db = get_connection()
        cursor = db.cursor()

        query = "UPDATE empDetails SET empName=%s, empDept=%s WHERE empId=%s"
        values = (name, dept, emp_id)

        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "Employee updated successfully!")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        db.close()
        resetfields()


def getData():
    emp_id = enterId.get()

    if not emp_id:
        messagebox.showwarning("Fetch Error", "Enter an ID to fetch data.")
        return

    try:
        db = get_connection()
        cursor = db.cursor()

        query = "SELECT empName, empDept FROM empDetails WHERE empID=%s"
        cursor.execute(query, (emp_id,))

        row = cursor.fetchone()

        if row:
            enterName.insert(0, row[0])
            enterDept.insert(0, row[1])
        else:
            messagebox.showinfo("Not Found", "No employee found with that ID.")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        db.close()


def deleteData():
    emp_id = enterId.get()

    if not emp_id:
        messagebox.showwarning("Delete Error", "Enter an ID to delete.")
        return

    try:
        db = get_connection()
        cursor = db.cursor()

        query = "DELETE FROM empDetails WHERE empID=%s"
        cursor.execute(query, (emp_id,))
        db.commit()

        messagebox.showinfo("Deleted", "Employee deleted successfully.")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        db.close()
        resetfields()


def show():
    try:
        db = get_connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM empDetails")
        rows = cursor.fetchall()

        showData.delete(0, END)

        for row in rows:
            showData.insert(END, f"{row[0]}  {row[1]}  {row[2]}")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        db.close()


def resetfields():
    enterId.delete(0, END)
    enterName.delete(0, END)
    enterDept.delete(0, END)


window = Tk()
window.geometry("500x300")
window.title("Employee CRUD App")

Label(window, text="Employee ID:", font=("Serif", 12)).place(x=20, y=30)
Label(window, text="Employee Name:", font=("Serif", 12)).place(x=20, y=70)
Label(window, text="Employee Dept:", font=("Serif", 12)).place(x=20, y=110)

enterId = Entry(window, width=25)
enterId.place(x=170, y=30)

enterName = Entry(window, width=25)
enterName.place(x=170, y=70)

enterDept = Entry(window, width=25)
enterDept.place(x=170, y=110)

Button(window, text="Insert", width=10, command=insertData).place(x=20, y=160)
Button(window, text="Update", width=10, command=updateData).place(x=110, y=160)
Button(window, text="Fetch", width=10, command=getData).place(x=200, y=160)
Button(window, text="Delete", width=10, command=deleteData).place(x=290, y=160)
Button(window, text="Reset", width=10, command=resetfields).place(x=150, y=210)
Button(window, text="Show All", width=10, command=show).place(x=240, y=210)

showData = Listbox(window, width=40)
showData.place(x=350, y=30)

window.mainloop()