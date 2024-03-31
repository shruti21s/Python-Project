import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import random

class GymMembershipApp:
    def __init__(self, master):
        self.master = master
        self.conn = sqlite3.connect('gym_database.db')
        self.c = self.conn.cursor()
        self.create_database_table()
        self.master.title("Gym Membership App")
        self.master.configure(bg='#F0F0F0')

        self.label_font = ('Helvetica', 20)
        self.button_font = ('Helvetica', 20)

        self.title_label = tk.Label(self.master, text="Dynamic Athletic Club", font=('Helvetica', 24, 'bold'), bg='#6C3483', fg='white', padx=10, pady=10)
        self.title_label.pack(fill=tk.X)

        self.menu_frame = tk.Frame(self.master, bg='#F0F0F0')
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        self.details_button = tk.Button(self.menu_frame, text="Enter Details", command=self.open_details_window, font=self.button_font, bg='#6C3483', fg='white')
        self.details_button.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.plans_button = tk.Button(self.menu_frame, text="Membership Plans", command=self.open_plans_window, font=self.button_font, bg='#6C3483', fg='white')
        self.plans_button.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.payment_button = tk.Button(self.menu_frame, text="Mode of Payment", command=self.open_payment_window, font=self.button_font, bg='#6C3483', fg='white')
        self.payment_button.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        self.view_db_button = tk.Button(self.menu_frame, text="View Database", command=self.view_database, font=self.button_font, bg='#6C3483', fg='white')
        self.view_db_button.grid(row=0, column=3, padx=10, pady=10, sticky='nsew')

        self.slogan_frame = tk.Frame(self.master, bg='#F0F0F0')
        self.slogan_frame.pack(fill=tk.BOTH, expand=True)

        self.slogan_label2 = tk.Label(self.slogan_frame, text="Fitness is not about being better than someone else. It's about being better than you used to be.", font=('Helvetica', 20), bg='#F0F0F0', fg='#6C3483')
        self.slogan_label2.pack(pady=(20, 10))

        self.slogan_label = tk.Label(self.slogan_frame, text="Get Fit, Stay Fit!", font=('Helvetica', 26), bg='#F0F0F0', fg='#6C3483')
        self.slogan_label.pack(pady=(10, 20))

        self.confirm_button = tk.Button(self.master, text="Confirm and Exit", command=self.confirm_and_exit, font=self.button_font, bg='#6C3483', fg='white')
        self.confirm_button.pack(pady=20, fill=tk.X)

        self.result_text = tk.StringVar()


    def create_database_table(self):
        self.c.execute('''
                      CREATE TABLE IF NOT EXISTS members (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT,
                          age INTEGER,
                          plan TEXT,
                          payment_mode TEXT
                      )
                      ''')
        self.conn.commit()

    def view_database(self):
        view_window = tk.Toplevel(self.master)
        view_window.title("Database View")

        self.c.execute("SELECT * FROM members")
        data = self.c.fetchall()

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                label = tk.Label(view_window, text=value, font=self.label_font)
                label.grid(row=i, column=j, padx=10, pady=5)

    def submit_details(self, name, age, email):
        error_messages = []

        if not all((name, age, email)):
            error_messages.append("Please fill in all fields")

        if not name.isalpha():
            error_messages.append("Name should contain only alphabets")

        try:
            age = int(age)
        except ValueError:
            error_messages.append("Age must be a number")

        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_pattern.match(email):
            error_messages.append("Invalid email format")

        if error_messages:
            messagebox.showerror("Error", "\n".join(error_messages))
            return

        self.c.execute("SELECT * FROM members WHERE name = ? AND age = ?", (name, age))
        existing_member = self.c.fetchone()
        if existing_member:
            messagebox.showerror("Error", "Member with the same name and age already exists")
            return

        details_result = f"Details Submitted:\nName: {name}\nAge: {age}\nEmail: {email}"
        self.result_text.set(details_result)
        messagebox.showinfo("Details Submitted", details_result)

        self.c.execute("INSERT INTO members (name, age) VALUES (?, ?)", (name, age))
        self.conn.commit()

    def open_details_window(self):
        details_window = tk.Toplevel(self.master)
        details_window.title("Details Form")

        label_name = tk.Label(details_window, text="Name:", font=self.label_font)
        label_name.grid(row=0, column=0, padx=30, pady=20, sticky=tk.W)
        entry_name = tk.Entry(details_window)
        entry_name.grid(row=0, column=1, padx=30, pady=20)

        label_age = tk.Label(details_window, text="Age:", font=self.label_font)
        label_age.grid(row=1, column=0, padx=30, pady=20, sticky=tk.W)
        entry_age = tk.Entry(details_window)
        entry_age.grid(row=1, column=1, padx=30, pady=20)

        label_email = tk.Label(details_window, text="Email:", font=self.label_font)
        label_email.grid(row=2, column=0, padx=30, pady=20, sticky=tk.W)
        entry_email = tk.Entry(details_window)
        entry_email.grid(row=2, column=1, padx=30, pady=20)

        submit_button = tk.Button(details_window, text="Submit Details", command=lambda: self.submit_details(entry_name.get(), entry_age.get(), entry_email.get()), font=self.button_font, bg='#6C3483', fg='white')
        submit_button.grid(row=3, column=0, columnspan=2, pady=6)

   
    def open_details_window(self):
        details_window = tk.Toplevel(self.master)
        details_window.title("Details Form")

        label_name = tk.Label(details_window, text="Name:", font=self.label_font)
        label_name.grid(row=0, column=0, padx=30, pady=20, sticky=tk.W)
        entry_name = tk.Entry(details_window)
        entry_name.grid(row=0, column=1, padx=30, pady=20)

        label_age = tk.Label(details_window, text="Age:", font=self.label_font)
        label_age.grid(row=1, column=0, padx=30, pady=20, sticky=tk.W)
        entry_age = tk.Entry(details_window)
        entry_age.grid(row=1, column=1, padx=30, pady=20)

        label_email = tk.Label(details_window, text="Email:", font=self.label_font)
        label_email.grid(row=2, column=0, padx=30, pady=20, sticky=tk.W)
        entry_email = tk.Entry(details_window)
        entry_email.grid(row=2, column=1, padx=30, pady=20)

        submit_button = tk.Button(details_window, text="Submit Details", command=lambda: self.submit_details(entry_name.get(), entry_age.get(), entry_email.get()), font=self.button_font, bg='#6C3483', fg='white')
        submit_button.grid(row=3, column=0, columnspan=2, pady=6)

    def open_plans_window(self):
       plans_window = tk.Toplevel(self.master)
       plans_window.title("Membership Plans")

       var = tk.IntVar()

       basic_plan = tk.Radiobutton(plans_window, text="Basic Plan - Rs1000/month", variable=var, value=1, font=self.label_font)
       basic_plan.grid(row=0, column=0, padx=20, pady=10, sticky=tk.W)

       standard_plan = tk.Radiobutton(plans_window, text="Standard Plan - Rs5000/month", variable=var, value=2, font=self.label_font)
       standard_plan.grid(row=1, column=0, padx=20, pady=10, sticky=tk.W)
                       
       premium_plan = tk.Radiobutton(plans_window, text="Premium Plan - Rs12000/month", variable=var, value=3, font=self.label_font)
       premium_plan.grid(row=2, column=0, padx=20, pady=10, sticky=tk.W)

       submit_button = tk.Button(plans_window, text="Submit Plan", command=lambda: self.submit_plan(var.get()), font=self.button_font)
       submit_button.grid(row=3, column=0, columnspan=2, pady=6)


    def submit_plan(self, selected_plan):
        if selected_plan == 1:
            plan_name = "Basic Plan"
            plan_price = "Rs1000/month"
        elif selected_plan == 2:
            plan_name = "Standard Plan"
            plan_price = "Rs5000/month"
        elif selected_plan == 3:
            plan_name = "Premium Plan"
            plan_price = "Rs12000/month"
        else:
            messagebox.showerror("Error", "Please select a membership plan.")
            return

        plan_result = f"Selected Plan: {plan_name}\nPrice: {plan_price}"
        self.result_text.set(plan_result)
        messagebox.showinfo("Plan Selected", plan_result)

        self.c.execute("UPDATE members SET plan = ? WHERE id = (SELECT MAX(id) FROM members)", (plan_name,))
        self.conn.commit()

    def open_payment_window(self):
        payment_window = tk.Toplevel(self.master)
        payment_window.title("Mode of Payment")

        var = tk.IntVar()

        cash = tk.Radiobutton(payment_window, text="Cash", variable=var, value=1, font=self.label_font)
        cash.grid(row=0, column=0, padx=30, pady=20, sticky=tk.W)

        cheque = tk.Radiobutton(payment_window, text="Cheque", variable=var, value=2, font=self.label_font)
        cheque.grid(row=0, column=1, padx=30, pady=20, sticky=tk.W)

        online_payment = tk.Radiobutton(payment_window, text="Online Payment", variable=var, value=3, font=self.label_font)
        online_payment.grid(row=1, column=0, padx=30, pady=20, sticky=tk.W)

        submit_button = tk.Button(payment_window, text="Submit Payment", command=lambda: self.submit_payment(var.get()), font=self.button_font)
        submit_button.grid(row=2, column=0, columnspan=2, pady=60)

    def submit_payment(self, selected_payment):
        if selected_payment == 1:
            payment_method = "Cash"
        elif selected_payment == 2:
            payment_method = "Cheque"
        elif selected_payment == 3:
            payment_method = "Online Payment"
        else:
            messagebox.showerror("Error", "Please select a payment method.")
            return

        payment_result = f"Selected Payment Method: {payment_method}"
        self.result_text.set(payment_result)
        messagebox.showinfo("Payment Method Selected", payment_result)

        self.c.execute("UPDATE members SET payment_mode = ? WHERE id = (SELECT MAX(id) FROM members)", (payment_method,))
        self.conn.commit()


    def confirm_and_exit(self):
        confirm_result = self.result_text.get()
        if confirm_result:
            messagebox.showinfo("Confirmation", f"Thank you!\n{confirm_result}\n\nExiting the app.")
        else:
            messagebox.showinfo("Confirmation", "Exiting the app.")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GymMembershipApp(root)
    root.mainloop()







        
            
