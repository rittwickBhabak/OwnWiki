import os
from state import State
from screens import CreateScreen, EditScreen, ListScreen, ViewScreen, CreateViewScreen, EditViewScreen
from tkinter import * 

if __name__=='__main__':
    BASE_DIR = os.getcwd()

    root = Tk()
    root.geometry('1500x700')
    # root.resizable(False, False)

    state = State(base_dir=BASE_DIR)
    list_screen = {
        'screen': ListScreen(root, state, 'OwnWiki - Welcome', 'OwnWiki - All Articles', True),
        'name': 'list_screen'
    }
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
    state.add_screen(list_screen)
    state.add_screen(create_screen)
    state.add_screen(view_screen)
    state.add_screen(edit_screen)
    state.show({'screen_name':'list_screen'})

    root.mainloop()
