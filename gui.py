import tkinter as tk
from tkinter import messagebox
from functions import *


def start_gui():
    window = tk.Tk()
    window.title("Employee Management System")
    window.geometry("550x450")
    window.configure(bg="#00334C")
    window.resizable(False, False)

    LABEL_FONT = ("Segoe UI", 11, "bold")
    ENTRY_FONT = ("Segoe UI", 11)
    BUTTON_FONT = ("Segoe UI", 10, "bold")

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
        
        if success:
            resetfields()

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
            showData.insert(tk.END, f"{r[0]} |  {r[1]}  |  {r[2]}")

    title = tk.Label(window, text="Employee Management System", font=("Segoe UI", 16, "bold"), bg="#00334C", fg="#00f7ff")
    title.grid(row=0, column=0, columnspan=2, pady=(10, 0))

    left_frame = tk.Frame(window, bg="#00334C")
    left_frame.grid(row=1, column=0, padx=20, pady=20, sticky="n")

    right_frame = tk.Frame(window, bg="#00334C")
    right_frame.grid(row=1, column=1, padx=10, pady=20)

    tk.Label(left_frame, text="Employee ID", font=LABEL_FONT, bg="#00334C", fg="white").grid(row=0, column=0, sticky="w", pady=5)
    enterId = tk.Entry(left_frame, font=ENTRY_FONT, width=25, bg="#f0f0f0",)
    enterId.grid(row=1, column=0, pady=5)

    tk.Label(left_frame, text="Employee Name", font=LABEL_FONT, bg="#00334C", fg="white").grid(row=2, column=0, sticky="w", pady=5)
    enterName = tk.Entry(left_frame, font=ENTRY_FONT, width=25, bg="#f0f0f0")
    enterName.grid(row=3, column=0, pady=5)

    tk.Label(left_frame, text="Department", font=LABEL_FONT, bg="#00334C", fg="white").grid(row=4, column=0, sticky="w", pady=5)
    enterDept = tk.Entry(left_frame, font=ENTRY_FONT, width=25, bg="#f0f0f0")
    enterDept.grid(row=5, column=0, pady=5)

    btn_frame = tk.Frame(left_frame, bg="#00334C")
    btn_frame.grid(row=6, column=0, pady=15)

    def styled_btn(text, cmd, color):
        return tk.Button(btn_frame, text=text, command=cmd, width=12, bg=color, fg="black", font=BUTTON_FONT, bd=0, relief="flat", activebackground=color)

    styled_btn("Insert", insertData, "#0099FF").grid(row=0, column=0, padx=5, pady=7)
    styled_btn("Update", updateData, "#11ff00").grid(row=0, column=1, padx=5, pady=7)
    styled_btn("Fetch", fetchData, "#ff00fb").grid(row=1, column=0, padx=5, pady=7)
    styled_btn("Delete", deleteData, "#ffff00").grid(row=1, column=1, padx=5, pady=7)
    styled_btn("Reset", resetfields, "#ff0000").grid(row=2, column=0, padx=5, pady=7)
    styled_btn("Show All", show, "#00eeff").grid(row=2, column=1, padx=5, pady=7)

    tk.Label(right_frame, text="Employee Records",
             font=("Segoe UI", 12, "bold"), bg="#00334C", fg="white").pack(anchor="w")

    showData = tk.Listbox(right_frame, width=35, height=19, font=("Consolas", 10), bg="#f0f0f0", bd=0, highlightthickness=1)
    showData.pack(pady=10)

    window.mainloop()
