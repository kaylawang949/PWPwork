from tkinter import *
from tkinter import messagebox

# simplifies message boxes by creating a separate file
# with them, then calling the message function

def login(username):
    messagebox.showinfo(message=f'Login successful! Welcome {username}.')

def create_acc():
    messagebox.showinfo(message=f'Account creation successful!')

def wrong_pw():
    messagebox.showinfo(message='Invalid password. Please try again.')

def invalid_user():
    messagebox.showinfo(message='Invalid username. Please try again.')

def user_exists():
    messagebox.showinfo(message='Account with this username already exists.')

def blank_entry():
    messagebox.showinfo(message='One or more entries were left blank. Please try again.')
