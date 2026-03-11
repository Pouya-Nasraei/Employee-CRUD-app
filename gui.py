import tkinter as tk
from tkinter import messagebox
from functions import *


def start_gui():

    window = tk.Tk()
    window.geometry("550x350")
    window.title("Employee CRUD App")

    def resetfields():
        enterId.delete(0, tk.END)
        enterName.delete(0, tk.END)
        enterDept.delete(0, tk.END)

    def insertData():

        emp_id = enterId.get().strip()
        name = enterName.get().strip()
        dept = enterDept.get().strip()

        if not emp_id or not name or not dept:
            messagebox.showwarning("Error", "All fields required")
            return

        success, msg = insert_employee(emp_id, name, dept)

        messagebox.showinfo("Result", msg)

        if success:
            resetfields()

    def updateData():

        emp_id = enterId.get().strip()
        name = enterName.get().strip()
        dept = enterDept.get().strip()

        success, msg = update_employee(emp_id, name, dept)

        messagebox.showinfo("Result", msg)

    def fetchData():

        emp_id = enterId.get().strip()

        row = get_employee(emp_id)

        if row:
            resetfields()
            enterId.insert(0, emp_id)
            enterName.insert(0, row[0])
            enterDept.insert(0, row[1])
        else:
            messagebox.showinfo("Result", "Employee not found")

    def deleteData():

        emp_id = enterId.get().strip()

        if delete_employee(emp_id):
            messagebox.showinfo("Deleted", "Employee removed")
            resetfields()
        else:
            messagebox.showinfo("Result", "Employee not found")

    def show():

        rows = get_all_employees()

        showData.delete(0, tk.END)

        for r in rows:
            showData.insert(tk.END, f"{r[0]}  {r[1]}  {r[2]}")

    tk.Label(window, text="Employee ID:").place(x=20, y=30)
    tk.Label(window, text="Employee Name:").place(x=20, y=70)
    tk.Label(window, text="Employee Dept:").place(x=20, y=110)

    enterId = tk.Entry(window, width=25)
    enterId.place(x=170, y=30)

    enterName = tk.Entry(window, width=25)
    enterName.place(x=170, y=70)

    enterDept = tk.Entry(window, width=25)
    enterDept.place(x=170, y=110)

    tk.Button(window, text="Insert", width=10, command=insertData).place(x=40, y=160)
    tk.Button(window, text="Update", width=10, command=updateData).place(x=130, y=160)
    tk.Button(window, text="Fetch", width=10, command=fetchData).place(x=220, y=160)

    tk.Button(window, text="Delete", width=10, command=deleteData).place(x=40, y=210)
    tk.Button(window, text="Reset", width=10, command=resetfields).place(x=130, y=210)
    tk.Button(window, text="Show All", width=10, command=show).place(x=220, y=210)

    showData = tk.Listbox(window, width=40)
    showData.place(x=350, y=30)

    window.mainloop()