import tkinter as tk
from tkinter import messagebox

class ATM_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Machine")
        self.root.geometry("400x400")

        # Initialize ATM functionality
        self.bank = Bank()
        self.bank.create_account("CHARAN", 1000.0, "1234")  # Pre-defined account
        self.current_user = None

        # Create frames for different pages
        self.login_frame = tk.Frame(self.root)
        self.options_frame = tk.Frame(self.root)

        self.login_frame.pack()
        self.options_frame.pack()

        # Start with the login frame visible and options frame hidden
        self.show_login_frame()
        self.hide_options_frame()

    def show_login_frame(self):
        self.login_frame.pack()
        self.hide_options_frame()

        # Create labels and entry widgets for login
        label_user_id = tk.Label(self.login_frame, text="User ID:")
        label_user_id.pack()
        self.entry_user_id = tk.Entry(self.login_frame)
        self.entry_user_id.pack()

        label_pin = tk.Label(self.login_frame, text="PIN:")
        label_pin.pack()
        self.entry_pin = tk.Entry(self.login_frame, show="*")
        self.entry_pin.pack()

        button_login = tk.Button(self.login_frame, text="Login", command=self.login)
        button_login.pack()

    def hide_login_frame(self):
        self.login_frame.pack_forget()
        self.entry_user_id.pack_forget()
        self.entry_pin.pack_forget()

    def show_options_frame(self):
        self.options_frame.pack()

        self.show_balance_button = tk.Button(self.options_frame, text="Check Balance", command=self.check_balance)
        self.show_balance_button.pack()

        self.withdraw_button = tk.Button(self.options_frame, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack()

        self.deposit_button = tk.Button(self.options_frame, text="Deposit", command=self.deposit)
        self.deposit_button.pack()

        self.transfer_button = tk.Button(self.options_frame, text="Transfer", command=self.transfer)
        self.transfer_button.pack()

        self.transaction_history_button = tk.Button(self.options_frame, text="Transaction History", command=self.view_transaction_history)
        self.transaction_history_button.pack()

        self.quit_button = tk.Button(self.options_frame, text="Quit", command=self.quit)
        self.quit_button.pack()

        self.back_button = tk.Button(self.options_frame, text="Back", command=self.show_login_frame)
        self.back_button.pack()

    def hide_options_frame(self):
        self.options_frame.pack_forget()
        self.show_balance_button.pack_forget()
        self.withdraw_button.pack_forget()
        self.deposit_button.pack_forget()
        self.transfer_button.pack_forget()
        self.transaction_history_button.pack_forget()
        self.quit_button.pack_forget()
        self.back_button.pack_forget()

    def login(self):
        user_id = self.entry_user_id.get()
        pin = self.entry_pin.get()
        account = self.bank.get_account(user_id)

        if account and account.pin == pin:
            self.current_user = account
            self.hide_login_frame()
            self.show_options_frame()
            self.update_balance()
            messagebox.showinfo("Login", "Login successful!")
        else:
            messagebox.showerror("Login Error", "Invalid user ID or PIN. Please try again.")

    def update_balance(self):
        if self.current_user:
            self.show_balance_button.config(text="Check Balance (Current Balance: ${:.2f})".format(self.current_user.balance))

    def check_balance(self):
        if self.current_user:
            messagebox.showinfo("Balance", "Current Balance: ${:.2f}".format(self.current_user.balance))
        else:
            messagebox.showerror("Balance Error", "Please log in first.")

    def deposit(self):
        if self.current_user:
            amount = float(self.entry_deposit.get())
            self.current_user.deposit(amount)
            self.update_balance()

    def withdraw(self):
        if self.current_user:
            amount = float(self.entry_withdraw.get())
            self.current_user.withdraw(amount)
            self.update_balance()

    def transfer(self):
        if self.current_user:
            amount = float(self.entry_transfer.get())
            target_account_number = self.entry_target_account.get()
            target_account = self.bank.get_account(target_account_number)

            if target_account:
                self.current_user.transfer(amount, target_account)
                self.update_balance()
            else:
                messagebox.showerror("Transfer Error", f"Target account {target_account_number} not found.")

    def view_transaction_history(self):
        if self.current_user:
            transactions = self.current_user.transaction_history
            if transactions:
                history_text = "Transaction History:\n"
                for transaction in transactions:
                    history_text += f"Type: {transaction.transaction_type}, Amount: ${0:.2f}\n"
                messagebox.showinfo("Transaction History", history_text)
            else:
                messagebox.showinfo("Transaction History", "No transactions found.")
        else:
            messagebox.showerror("Transaction History", "Please log in first.")

    def quit(self):
        self.root.destroy()

class Transaction:
    def __init__(self, transaction_id, date, time, amount, transaction_type):
        self.transaction_id = transaction_id
        self.date = date
        self.time = time
        self.amount = amount
        self.transaction_type = transaction_type

class Account:
    def __init__(self, account_number, balance, pin):
        self.account_number = account_number
        self.balance = balance
        self.pin = pin
        self.transaction_history = []

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(Transaction(len(self.transaction_history) + 1, "date", "time", amount, "Deposit"))

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transaction_history.append(Transaction(len(self.transaction_history) + 1, "date", "time", amount, "Withdrawal"))

    def transfer(self, amount, target_account):
        if self.balance >= amount:
            self.balance -= amount
            target_account.deposit(amount)
            self.transaction_history.append(Transaction(len(self.transaction_history) + 1, "date", "time", amount, "Transfer"))

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, balance, pin):
        account = Account(account_number, balance, pin)
        self.accounts[account_number] = account

    def get_account(self, account_number):
        return self.accounts.get(account_number)

if __name__ == "__main__":
    root = tk.Tk()
    atm_gui = ATM_GUI(root)
    root.mainloop()
