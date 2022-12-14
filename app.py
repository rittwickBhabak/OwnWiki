'''This is the starting point of the application.

This module contains the main window of the application.

'''


import os
from state import State
from screens import CreateScreen, EditScreen, ListScreen, ViewScreen, CreateViewScreen, EditViewScreen
from tkinter import * 

def main():
    '''Starting point of the application.
    
    In this function, all of the screens are created, the state object is \
        created and the screens are attached to the state object. 
    And on startup the list_screen is shown.
    
    '''
    
    BASE_DIR = os.getcwd()

    root = Tk()
    root.geometry('1500x600')
    root.minsize(1500, 600)
    # root.resizable(False, False)

    state = State(base_dir=BASE_DIR)
    create_screen = {
        'screen': CreateViewScreen(root, state, 'Create New Article', '', False),
        'name': 'create_screen'
    }
    view_screen = {
        'screen': ViewScreen(root, state, 'Read Article', '', False),
        'name': 'view_screen'
    }
    edit_screen = {
        'screen': EditViewScreen(root, state, 'Edit Article', '', False),
        'name': 'edit_screen'
    }
    list_screen = {
        'screen': ListScreen(root, state, 'OwnWiki - Welcome', 'OwnWiki - All Articles', True),
        'name': 'list_screen'
    }
    state.add_screen(create_screen)
    state.add_screen(view_screen)
    state.add_screen(edit_screen)
    state.add_screen(list_screen)
    state.show({'screen_name':'list_screen'})

    root.mainloop()

if __name__=='__main__':
    main()