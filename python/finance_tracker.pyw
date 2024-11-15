import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("600x400")
        self.root.configure(bg='#2e2e2e')

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))

        self.income_label = ttk.Label(self.root, text="Income:", background='#2e2e2e', foreground='white')
        self.income_label.grid(row=0, column=0, padx=10, pady=10)
        self.income_entry = ttk.Entry(self.root, width=30)
        self.income_entry.grid(row=0, column=1, padx=10, pady=10)

        self.expense_label = ttk.Label(self.root, text="Expense:", background='#2e2e2e', foreground='white')
        self.expense_label.grid(row=1, column=0, padx=10, pady=10)
        self.expense_entry = ttk.Entry(self.root, width=30)
        self.expense_entry.grid(row=1, column=1, padx=10, pady=10)

        self.category_label = ttk.Label(self.root, text="Category:", background='#2e2e2e', foreground='white')
        self.category_label.grid(row=2, column=0, padx=10, pady=10)
        self.category_entry = ttk.Entry(self.root, width=30)
        self.category_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = ttk.Button(self.root, text="Add Entry", command=self.add_entry)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=('Type', 'Amount', 'Category', 'Date'), show='headings')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Date', text='Date')
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.summary_frame = ttk.Frame(self.root)
        self.summary_frame.grid(row=5, column=0, columnspan=2, pady=10)
        self.summary_label = ttk.Label(self.summary_frame, text="", background='#2e2e2e', foreground='white', font=("Arial", 12))
        self.summary_label.pack()

    def add_entry(self):
        income = self.income_entry.get().strip()
        expense = self.expense_entry.get().strip()
        category = self.category_entry.get().strip()

        if not income and not expense:
            messagebox.showerror("Error", "Please enter an income or expense.")
            return

        entry_type = 'Income' if income else 'Expense'
        amount = income if income else expense

        self.tree.insert('', 'end', values=(entry_type, amount, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.save_data(entry_type, amount, category)
        self.income_entry.delete(0, tk.END)
        self.expense_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.update_summary()

    def save_data(self, entry_type, amount, category):
        with open('finance_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([entry_type, amount, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    def load_data(self):
        try:
            with open('finance_data.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.tree.insert('', 'end', values=row)
            self.update_summary()
        except FileNotFoundError:
            with open('finance_data.csv', 'w') as file:
                pass

    def update_summary(self):
        total_income = 0
        total_expense = 0
        for row in self.tree.get_children():
            row_data = self.tree.item(row)['values']
            if row_data[0] == 'Income':
                total_income += float(row_data[1])
            else:
                total_expense += float(row_data[1])

        balance = total_income - total_expense
        self.summary_label.config(text=f"Total Income: {total_income}\nTotal Expense: {total_expense}\nBalance: {balance}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()
