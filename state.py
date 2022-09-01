'''This modules holds the state of the screen.

All of the screen has to be registered to the State class object.

'''


from tkinter import * 

class State():
    '''All of the screen has to registered to the state class object.
    
    All of the showing and hiding of the screens will be happened through this\
        state object.

    Attributes:
        base_dir: An path object indicating the root directory of the project.

        screens: List of screens
    
    Methods:
        add_screen: Adds screen to the screen list

        show: Calls the show method of a screen.

    '''

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.screens = [] # items: {'name': str (unique), 'screen': ptr2screen_obj}

    def add_screen(self, screen):
        '''Adds screen to the screen list.
        
        Arguments:
            screen: A screen object
        
        Returns:
            None

        '''
        self.screens.append(screen)

    def show(self, options=None, event=None):
        '''Call the show method a the specified screen.

        Arguments:
            options: A dictionary of type \
                {'screen_name': string, 'file_name':a string specifying article}

            event: An event, automatically passed by the invoked function
        '''

        screen_to_show = None 
        for screen in self.screens:
            if screen['name']==options.get('screen_name'):
                screen_to_show = screen 
                screen['screen'].hide()
            else:
                screen['screen'].hide()
        if screen_to_show is not None:
            screen_to_show.get('screen').show(options)