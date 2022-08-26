import os
from functools import partial
from abc import ABC, abstractmethod

from tkinter import *

import data_manager
from renderer import Renderer
from messages import show_message, askquestion


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
        value = self.make_screen_elements(options)
        if value is None or value==1:
            for element in self.screen_elements:
                element['element'].pack(**element['pack_options']) 

    @abstractmethod
    def make_screen_elements(self, options=None):
        pass 

    def hide(self, *args, **kwargs):
        self.set_active(False)
        for element in self.screen_elements:
            try:
                element['element'].pack_forget()
            except:
                pass 
            element['element'].destroy()
        self.screen_elements = []

class ListScreen(Screen):

    def __init__(self, root, state, title, heading, is_active=False):
        super().__init__(root=root, state=state, title=title, heading=heading, is_active=is_active)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def set_file_paths(self):
        self.current_md_files = data_manager.get_articles_list()

    def make_screen_elements(self, options=None):    
        self.wrapper = LabelFrame(self.root)
        self.canvas = Canvas(self.wrapper)
        self.yscrollbar = Scrollbar(self.wrapper, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.yscrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)


        self.heading_label = Label(self.root, text=self.heading, font='comicsansms 22 bold')
        self.add_element(element=self.heading_label, pack_options={'side': TOP, 'pady': 10})

        self.frame = Frame(self.canvas, padx=70, pady=20)
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')

        self.add_element(element=self.canvas, pack_options={'side':LEFT, 'fill':BOTH, 'expand':True})
        self.add_element(element=self.yscrollbar, pack_options={'fill':Y, 'side':RIGHT})

        # self.add_element(element=self.frame, pack_options={'side':LEFT, 'anchor':'nw', 'fill':Y, 'ipadx':20, 'ipady':20})

        self.view_links = []
        self.set_file_paths()

        for index, md_file in enumerate(self.current_md_files):
            label = Label(self.frame, text=f'{index+1}. {md_file[:-3].title()}', font='comicsansms 18')
            self.view_links.append(label)
            label.bind('<Button-1>', partial(self.state.show, {'screen_name':'view_screen', 'article_name': md_file[:-3]}))
            self.add_element(element=label, pack_options={'anchor':'w'})
        
        self.create_link = Label(self.frame, text=u'\u2022' + '  Create New Article', font='comicsansms 18')
        self.create_link.bind('<Button-1>', partial(self.state.show, {'screen_name': 'create_screen'}))

        self.add_element(element=self.create_link, pack_options={'anchor':'w'})
        self.add_element(element=self.wrapper, pack_options={'fill':BOTH, 'ipadx':20, 'ipady':20, 'expand':True})

class CreateScreen(Screen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_data_before_save(self, file_name, file_content, action):
        response = data_manager.check_data(file_name, file_content, action)
        code = response['code']
        message = response.get('message')
        # responses can be
        # 1. file name blank
        # 2. duplicate file name
        # 3. file content blank
        if code==1: # article name blank
            show_message('Error', message)
            return
        elif code==2: # duplicate article name
            value = askquestion('Warning', message)
            if value=='yes': # overwrite the existing article
                data_manager.edit(file_name, file_content)
                self.state.show({'screen_name': 'view_screen', 'article_name': file_name})
                return
            else: # edit the existing article, loose the current state
                self.state.show({'screen_name': 'edit_screen', 'article_name': file_name})
                return
        elif code==3: # article content blank
            value = askquestion('Warning', message)
            if value=='yes': # save article with blank content
                data_manager.create_and_save(file_name, file_content)
                self.state.show({'screen_name': 'view_screen', 'article_name': file_name})
                return
            else:
                return
        return True
       
    def save(self, event):
        file_name = self.title_value.get()
        file_content = self.text.get("1.0", "end-1c")
        is_ok = self.check_data_before_save(file_name, file_content, action='create')
        if is_ok==True:
            data_manager.create_and_save(file_name, file_content)
            self.state.show({'screen_name': 'view_screen', 'article_name': file_name}) 

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
        self.save_button.bind('<Button-1>', self.save)

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
        show_message('Successfully Deleted The Article', f'{file_name} is deleted successfully')
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
            # self.text.insert(END, self.text_string)
            Renderer(self.text, self.text_string, self.state).render()
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
            show_message('Error', f"There is no article named '{options.get('article_name')}'")
            self.state.show({'screen_name': 'create_screen', 'article_name':options.get('article_name')})
            return -1

class EditScreen(CreateScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, event):
        file_name = self.title_value.get()
        file_content = self.text.get("1.0", "end-1c")
        is_ok = self.check_data_before_save(file_name, file_content, action='edit')
        if is_ok==True:
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
        self.save_button.bind('<Button-1>', self.save)
        self.title_entry.config(state='disabled')
        self.text.insert(END, self.get_article_content(options['article_name']))



class CreateViewScreen(CreateScreen, ViewScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def change_event_handler(self, event=None):
        self.view_text.config(state='normal')
        self.view_text.delete("1.0", "end")
        Renderer(self.view_text, self.edit_text.get("1.0", "end-1c"), self.state).render()
        self.view_text.config(state='disabled')
    
    def make_screen_elements(self, options=None):
        self.frame = Frame(self.root, padx=50, pady=10, borderwidth=1, relief=GROOVE)
        self.panes = Frame(self.root, padx=50, pady=10, borderwidth=1, relief=GROOVE)

        self.edit_frame = Frame(self.panes)
        self.view_frame = Frame(self.panes)

        self.edit_text = Text(self.edit_frame, font='comicsansms 15', padx=50, pady=20)
        self.text = self.edit_text
        self.view_text = Text(self.view_frame, font='comicsansms 15', padx=50, pady=20)
        self.change_event_handler()
        self.view_text.config(state='disabled')

        self.set_title('Create New Article')
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
        self.save_button.bind('<Button-1>', self.save)

        self.edit_text.bind("<KeyPress>", self.change_event_handler)
        self.edit_text.bind("<KeyRelease>", self.change_event_handler)

        self.add_element(element=self.frame, pack_options={'fill':X})
        self.add_element(element=self.title_label, pack_options={})
        self.add_element(element=self.title_entry, pack_options={'fill':X, 'pady':10, 'ipadx':10, 'ipady':10})
        self.add_element(element=self.home_button, pack_options={'side':LEFT})
        self.add_element(element=self.save_button, pack_options={'side':LEFT})

        self.add_element(element=self.panes, pack_options={'fill':BOTH, 'expand':True})
        self.add_element(element=self.edit_frame, pack_options={'fill':Y, 'side':LEFT, 'anchor':'nw'})
        self.add_element(element=self.view_frame, pack_options={'fill':Y, 'side':RIGHT, 'anchor':'ne'})
        self.add_element(element=self.edit_text, pack_options={'fill':BOTH, 'expand':True})
        self.add_element(element=self.view_text, pack_options={'fill':BOTH, 'expand':True})

class EditViewScreen(EditScreen, ViewScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def change_event_handler(self, event=None):
        self.view_text.config(state='normal')
        self.view_text.delete("1.0", "end")
        Renderer(self.view_text, self.edit_text.get("1.0", "end-1c"), self.state).render()
        self.view_text.config(state='disabled')
    
    def make_screen_elements(self, options=None):
        self.frame = Frame(self.root, padx=50, pady=10, borderwidth=1, relief=GROOVE)
        self.panes = Frame(self.root, padx=50, pady=10, borderwidth=1, relief=GROOVE)

        self.edit_frame = Frame(self.panes)
        self.view_frame = Frame(self.panes)

        self.edit_text = Text(self.edit_frame, font='comicsansms 15', padx=50, pady=20)
        self.text = self.edit_text
        self.view_text = Text(self.view_frame, font='comicsansms 15', padx=50, pady=20)
        self.view_text.config(state='normal')
        self.view_text.delete("1.0", "end")
        self.edit_text.insert(END, data_manager.get(options['article_name']))
        Renderer(self.view_text, data_manager.get(options['article_name']), self.state).render()
        self.view_text.config(state='disabled')
        self.view_text.config(state='disabled')

        self.set_title(f'Edit Article - {options["article_name"]}')
        self.title_label = Label(self.frame, text='Enter Title: ', font='comicsansms 22 bold', bg='white')
        self.title_value = StringVar()
        if options is not None:
            article_name = options.get('article_name')
            if article_name is not None:
                self.title_value.set(options['article_name'])

        self.title_entry = Entry(self.frame, textvariable=self.title_value, font='comicsansms 20', borderwidth=2, relief=GROOVE)
        self.title_entry.config(state='disabled')


        self.home_button = Button(self.frame, text='Home', padx=10, pady=5, font='comicsansms 10')
        self.home_button.bind('<Button-1>', partial(self.state.show, {'screen_name': 'list_screen'}))

        self.save_button = Button(self.frame, text='Save', padx=10, pady=5, font='comicsansms 10')
        self.save_button.bind('<Button-1>', self.save)

        self.edit_text.bind("<KeyPress>", self.change_event_handler)
        self.edit_text.bind("<KeyRelease>", self.change_event_handler)

        self.add_element(element=self.frame, pack_options={'fill':X})
        self.add_element(element=self.title_label, pack_options={})
        self.add_element(element=self.title_entry, pack_options={'fill':X, 'pady':10, 'ipadx':10, 'ipady':10})
        self.add_element(element=self.home_button, pack_options={'side':LEFT})
        self.add_element(element=self.save_button, pack_options={'side':LEFT})

        self.add_element(element=self.panes, pack_options={'fill':BOTH, 'expand':True})
        self.add_element(element=self.edit_frame, pack_options={'fill':Y, 'side':LEFT, 'anchor':'nw'})
        self.add_element(element=self.view_frame, pack_options={'fill':Y, 'side':RIGHT, 'anchor':'ne'})
        self.add_element(element=self.edit_text, pack_options={'fill':BOTH, 'expand':True})
        self.add_element(element=self.view_text, pack_options={'fill':BOTH, 'expand':True})


