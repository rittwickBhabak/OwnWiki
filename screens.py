from abc import ABC, abstractmethod
from tkinter import *
from functools import partial
import os 

class Screen(ABC):
    def __init__(self, root, state, title="", heading="", is_active=False):
        self.set_root(root)
        self.set_heading(heading)
        self.set_title(title) 
        self.set_state(state)
        self.set_active(is_active)

        self.screen_elements = [] # items: {'element': ptr_2_element, 'pack_options': dictionary}

    # setters
    def set_root(self, root):
        self.root = root 
    
    def set_title(self, title):
        self.title = title 
    
    def set_state(self, state):
        self.state = state 
    
    def set_heading(self, heading):
        self.heading = heading 

    def set_active(self, is_active):
        self.is_active = is_active

    def add_elements(self, ptr2element, pack_options):
        element = {'ptr2element': ptr2element,
                    'pack_options': pack_options}
        self.screen_elements.append(element)

    def show(self, *args, **kwargs):
        self.set_active(True)
        self.make_screen_elements()
        for element in self.screen_elements:
            element['element'].pack(**element['pack_options']) 

    @abstractmethod
    def make_screen_elements(self, *args, **kwargs):
        pass 

    def hide(self, *args, **kwargs):
        for element in self.screen_elements:
            element['element'].destroy()
            self.screen_elements.remove(element)

class ListScreen(Screen):

    def __init__(self, root, state, title, heading, is_active=False):
        super().__init__(root=root, state=state, title=title, heading=heading, is_active=is_active)

    def set_file_paths(self):
        dir_path = os.path.join(self.state.base_dir, 'data', 'mds')
        self.current_md_files = os.listdir(dir_path) 

    def make_screen_elements(self, *args, **kwargs):
        
        self.heading_label = Label(self.root, text=self.heading, font='comicsansms 22 bold')
        self.screen_elements.append({'element': self.heading_label, 'pack_options': {'side': TOP, 'pady': 10}})

        self.frame = Frame(self.root, padx=70, pady=20)
        self.screen_elements.append({'element': self.frame, 'pack_options': {'side':LEFT, 'anchor':'nw', 'fill':Y, 'ipadx':20, 'ipady':20}})

        self.view_links = []
        self.set_file_paths()
        dir_path = os.path.join(self.state.base_dir, 'data', 'mds')
        for index, md_file in enumerate(self.current_md_files):
            label = Label(self.frame, text=f'{index+1}. {md_file[:-3].title()}', font='comicsansms 18')
            self.view_links.append(label)
            # label.bind('<Button-1>', partial(self.state.show_article, dir_path, md_file[:-3]))
            self.screen_elements.append({'element': label, 'pack_options': {'anchor':'w'}})
        
        self.create_link = Label(self.frame, text=u'\u2022' + '  Create New Article', font='comicsansms 18')
        # self.create_link.bind('<Button-1>', partial(self.state.show_create, ''))

        self.screen_elements.append({'element': self.create_link, 'pack_options': {'anchor':'w'}})