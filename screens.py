from abc import ABC, abstractmethod
from tkinter import *
from functools import partial
import os
from typing import overload 
import data_manager

class Screen(ABC):

    def __init__(self, root, state, title="", heading="", is_active=False):
        self.set_root(root)
        self.set_heading(heading)
        self.set_title(title) 
        self.set_state(state)
        self.set_active(is_active)

        self.screen_elements = [] # items: {'element': ptr_2_element, 'pack_options': dictionary}

    def set_root(self, root):
        self.root = root 
    
    def set_title(self, title):
        self.root.title(title)
    
    def set_state(self, state):
        self.state = state 
    
    def set_heading(self, heading):
        self.heading = heading 

    def set_active(self, is_active):
        self.is_active = is_active

    def add_element(self, element, pack_options):
        element = {'element': element,
                    'pack_options': pack_options}
        self.screen_elements.append(element)

    def show(self, options=None):
        self.set_active(True)
        self.make_screen_elements(options)
        for element in self.screen_elements:
            element['element'].pack(**element['pack_options']) 

    @abstractmethod
    def make_screen_elements(self, options=None):
        pass 

    def hide(self, *args, **kwargs):
        self.set_active(False)
        for element in self.screen_elements:
            element['element'].pack_forget()
            element['element'].destroy()
        self.screen_elements = []

class ListScreen(Screen):

    def __init__(self, root, state, title, heading, is_active=False):
        super().__init__(root=root, state=state, title=title, heading=heading, is_active=is_active)

    def set_file_paths(self):
        self.current_md_files = data_manager.get_articles_list()

    def make_screen_elements(self, options=None):      
        self.heading_label = Label(self.root, text=self.heading, font='comicsansms 22 bold')
        self.add_element(element=self.heading_label, pack_options={'side': TOP, 'pady': 10})

        self.frame = Frame(self.root, padx=70, pady=20)
        self.add_element(element=self.frame, pack_options={'side':LEFT, 'anchor':'nw', 'fill':Y, 'ipadx':20, 'ipady':20})

        self.view_links = []
        self.set_file_paths()
        dir_path = os.path.join(self.state.base_dir, 'data', 'mds')
        for index, md_file in enumerate(self.current_md_files):
            label = Label(self.frame, text=f'{index+1}. {md_file[:-3].title()}', font='comicsansms 18')
            self.view_links.append(label)
            label.bind('<Button-1>', partial(self.state.show, {'screen_name':'view_screen', 'article_name': md_file[:-3]}))
            self.add_element(element=label, pack_options={'anchor':'w'})
        
        self.create_link = Label(self.frame, text=u'\u2022' + '  Create New Article', font='comicsansms 18')
        self.create_link.bind('<Button-1>', partial(self.state.show, {'screen_name': 'create_screen'}))

        self.add_element(element=self.create_link, pack_options={'anchor':'w'})

class CreateScreen(Screen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __save(self, event):
        file_name = self.title_value.get()
        file_content = self.text.get("1.0", "end-1c")
        data_manager.create_and_save(file_name, file_content)
        self.state.show({'screen_name':'view_screen', 'article_name':file_name})

    def make_screen_elements(self, options=None):

        self.set_title('Create New Article')

        self.text = Text(self.root, font='comicsansms 18', padx=50, pady=20)
        self.text_string = ''
        self.text.insert(END, self.text_string)

        self.frame = Frame(self.root, bg='white', padx=50, pady=10, borderwidth=1, relief=GROOVE)

        self.title_label = Label(self.frame, text='Enter Title: ', font='comicsansms 22 bold', bg='white')
        self.title_value = StringVar()
        if options is not None:
            article_name = options.get('article_name')
            if article_name is not None:
                self.title_value.set(options['article_name'])

        self.title_entry = Entry(self.frame, textvariable=self.title_value, font='comicsansms 20', borderwidth=2, relief=GROOVE)

        self.home_button = Button(self.frame, text='Home', padx=10, pady=5, font='comicsansms 10')
        self.home_button.bind('<Button-1>', partial(self.state.show, {'screen_name': 'list_screen'}))

        self.save_button = Button(self.frame, text='Save', padx=10, pady=5, font='comicsansms 10')
        self.save_button.bind('<Button-1>', self.__save)

        self.add_element(element=self.frame, pack_options={'fill':BOTH})
        self.add_element(element=self.title_label, pack_options={})
        self.add_element(element=self.title_entry, pack_options={'fill':X, 'pady':10, 'ipadx':10, 'ipady':10})
        self.add_element(element=self.home_button, pack_options={'side':LEFT})
        self.add_element(element=self.save_button, pack_options={'side':LEFT})
        self.add_element(element=self.text, pack_options={'expand':True, 'fill':BOTH})

class ViewScreen(Screen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __delete(self, event):
        file_name = self.heading.replace('Read Article - ', '')
        data_manager.delete(file_name)
        self.state.show({'screen_name':'list_screen'})

    def get_article_content(self, article_name):
        file_src = os.path.join(self.state.base_dir, 'data', 'mds', article_name+'.md')
        with open(file_src, 'r') as f:
            return f.read()
    
    def make_screen_elements(self, options=None):
        self.set_heading(f'Read Article - {options.get("article_name")}')
        self.set_title(f'Read Article - {options.get("article_name")}')

        self.text = Text(self.root, font='comicsansms 15', padx=50, pady=20)
        try:
            self.text_string = self.get_article_content(options.get('article_name'))
            self.text.insert(END, self.text_string)
            # Parser(self, self.text, self.text_string, self.state).parse()
            self.text.config(state='disabled')

            self.frame = Frame(self.root, bg='white', padx=50, pady=10, borderwidth=1, relief=GROOVE)

            self.heading_label = Label(self.frame, text=self.heading.title(), font='comicsansms 22 bold', bg='white')

            self.home_button = Button(self.frame, text='Home', padx=10, pady=5, font='comicsansms 10')
            self.home_button.bind('<Button-1>', partial(self.state.show, {'screen_name': 'list_screen'}))

            self.edit_button = Button(self.frame, text='Edit', padx=10, pady=5, font='comicsansms 10')
            self.edit_button.bind('<Button-1>', partial(self.state.show, {'screen_name':'edit_screen', 'article_name':self.heading.replace('Read Article - ', '')}))

            self.delete_button = Button(self.frame, text='Remove', padx=10, pady=5, font='comicsansms 10')
            self.delete_button.bind('<Button-1>', self.__delete)



            self.add_element(element=self.frame, pack_options={'fill':BOTH})
            self.add_element(element=self.heading_label, pack_options={})
            self.add_element(element=self.home_button, pack_options={'side':LEFT})
            self.add_element(element=self.edit_button, pack_options={'side':LEFT, 'padx':10})
            self.add_element(element=self.delete_button, pack_options={'side':LEFT})
            self.add_element(element=self.text, pack_options={'expand':True, 'fill':BOTH})


        except Exception as e:
            # new_file_name = os.path.basename(self.file_path)
            # self.state.showinfo('Error', str(e))
            # # self.state.showinfo('Error', f"There is no article named '{new_file_name[:-3]}'")

            # if new_file_name.endswith('.md'):
            #     self.state.show_create(os.path.basename(self.file_path)[:-3])
            # else:
            #     self.state.show_create(os.path.basename(self.file_path))
            print(f'ERROR!!! {e}')

class EditScreen(CreateScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __save(self, event):
        file_name = self.title_value.get()
        file_content = self.text.get("1.0", "end-1c")
        data_manager.edit(file_name, file_content)
        self.state.show({'screen_name':'view_screen', 'article_name':file_name})

    
    def get_article_content(self, article_name):
        file_src = os.path.join(self.state.base_dir, 'data', 'mds', article_name+'.md')
        with open(file_src, 'r') as f:
            return f.read()

    def make_screen_elements(self, options=None):
        super().make_screen_elements(options=options)
        self.set_heading(f'Edit Article - {options.get("article_name")}')
        self.set_title(f'Edit Article - {options.get("article_name")}')
        self.save_button.bind('<Button-1>', self.__save)
        self.title_entry.config(state='disabled')
        self.text.insert(END, self.get_article_content(options['article_name']))

