'''This module has the ability of showing messages and asking yes/no questions.'''


from tkinter import messagebox as tmsg 

def show_message(status, message):
    '''Shows messages to user.
    
    Arguments:
        status: string either 'error' or 'warning' or 'info'

        message: a string containing the message to show
    
    Returns: 
        None 

    '''

    if status=='error':
        tmsg.showerror('Error', message)
    elif status=='warning':
        tmsg.showwarning('Warning', message)
    else:
        tmsg.showinfo('Message', message)

def askquestion(status, message):
    '''Asks yes/no question to the user. 
    
    Arguments:
        message: a string containing the question to ask.
    
    Returns:
        None 

    '''
    
    value = tmsg.askquestion(status, message)
    return value 