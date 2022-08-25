from tkinter import messagebox as tmsg 

def show_message(status, message):
    if status=='error':
        tmsg.showerror('Error', message)
    elif status=='warning':
        tmsg.showwarning('Warning', message)
    else:
        tmsg.showinfo('Message', message)

def askquestion(status, message):
    value = tmsg.askquestion(status, message)
    return value 