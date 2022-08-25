from tkinter import * 

class State():
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.screens = [] # items: {'name': str (unique), 'screen': ptr2screen_obj}

    def add_screen(self, screen):
        self.screens.append(screen)

    def show(self, options=None, event=None):
        screen_to_show = None 
        for screen in self.screens:
            if screen['name']==options.get('screen_name'):
                screen_to_show = screen 
                screen['screen'].hide()
            else:
                screen['screen'].hide()
        if screen_to_show is not None:
            screen_to_show.get('screen').show(options)