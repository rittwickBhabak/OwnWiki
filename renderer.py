'''This module renders the raw string to the textarea.

The Renderer class takes raw content of the markdown file. Then removes the \
    unnecessary line breaks by creates a sanitized content in which per\
    line can be parsed independently. 

'''

from tkinter import * 
from tkinter import Text
from tkinter import font 
from functools import partial
from hyperlink_manager import HyperlinkManager
from parsers import parse 

class Renderer():
    '''The Renderer class takes raw content of the markdown file. 
    
    Then removes the unnecessary line breaks by creates a sanitized content\
    in which per line can be parsed independently. 
    
    Attributes:
        textarea: A Text widget where text is inserted after parsing.

        content: A string to be parsed.

        state: A state object to which screens are attached.
    
    Methods:
        create_tag: Creates tags for proper styling.
        
        content_2_blocks: Divides raw content to blocks to texts.
        
        block_2_sanitized_block: Remove unnecessary line breaks b/w the lines.
        
        sanitized_blocks_2_sanitized_content: Joins the sanitized blocks to make\
            sanitized contents.

        content_2_lines: Divides the sanitized content to lines.

        line_2_parsed_chars: Parsed the line to parsed list of chars.

        render_content: Adds the parsed list of chars to the textarea.

        render_line: Adds the parsed line to the textarea.

        render: Renders the complete content.

    '''

    def __init__(self, textarea, content, state):
        self.textarea = textarea
        self.content = content
        self.app_state = state
        self.hyperlink = HyperlinkManager(self.textarea)  
        self.sanitized_content = ''
        self.sanitized_blocks = []
        self.lines = []
        
    def create_tag(self, attrs):
        '''Creates tags for proper styling.
        
        Arguments:
            attrs: list of strings specifying the styles for a character

        Returns:
            None

        '''

        my_font = font.Font(self.textarea, self.textarea.cget('font'))
        attrs.sort()
        for attr in attrs:
            if attr=='bold':
                my_font.configure(weight="bold")
            elif attr=='italic':
                my_font.configure(slant='italic')
            elif attr=='underline':
                my_font.configure(underline=True)
            elif attr=='h1':
                my_font.configure(size=24)
            elif attr=='h2':
                my_font.configure(size=20)
        tag = '_'.join(attrs) 
        self.textarea.tag_configure(tag, font=my_font)
        return tag

    def content_2_blocks(self):
        '''Divides raw content to blocks to texts.
        
        Arguments:
            None

        Returns:
            None

        '''

        blocks = self.content.split('\n\n')
        return blocks 

    def block_2_sanitized_block(self, block):
        '''Remove unnecessary line breaks b/w the lines.
        
        Arguments:
            block: A string having unnecessary line breaks.

        Returns:
            None

        '''

        lines = block.split('\n')
        to_delete = False 
        for line_num, line in enumerate(lines):
            if to_delete:
                lines[line_num] = 'THIS_LINE_TO_BE_DELETED'
                to_delete = False 
            elif line_num+1<len(lines) and line.startswith('* ') and not lines[line_num+1].startswith('* ') and not lines[line_num+1].startswith('# ') and not lines[line_num+1].startswith('## '):
                lines[line_num] = lines[line_num] + ' ' + lines[line_num+1]
                to_delete = True

        lines = list(filter(lambda x: x!='THIS_LINE_TO_BE_DELETED', lines))

        for line_num in range(len(lines)-1, 0, -1):
            next = lines[line_num-1]
            current = lines[line_num]
            l1 = ['* ', '# ']
            l2 = ['## ']

            if current.strip()!='' and next.strip()!='' and (current[:2] not in l1) and (current[:3] not in l2) and (next[:2] not in l1) and (next[:3] not in l2):
                lines[line_num-1 ] = lines[line_num-1] + ' ' + lines[line_num]
                lines[line_num] = 'THIS_LINE_TO_BE_DELETED'

        lines = list(filter(lambda x: x!='THIS_LINE_TO_BE_DELETED', lines))

        return '\n'.join(lines) 

    def sanitized_blocks_2_sanitized_content(self):
        '''Joins the sanitized blocks to make\
            
            Arguments:
                None

            Returns:
                None

            '''

        self.content = '\n\n'.join(self.sanitized_blocks)

    def content_2_lines(self):
        '''Divides the sanitized content to lines.
        
        Arguments:
            None

        Returns:
            None

        '''

        self.lines = self.content.split('\n') 

    def line_2_parsed_chars(self, line):
        '''Parsed the line to parsed list of chars.
        
        Arguments:
            line: An raw string

        Returns:
            The list of parsed characters.

        '''

        return parse(line)

    def render_content(self):
        '''Adds the parsed list of chars to the textarea.
        
        Arguments:
            None

        Returns:
            None

        '''

        blocks = self.content_2_blocks()
        for block in blocks:
            self.sanitized_blocks.append(self.block_2_sanitized_block(block))
        self.sanitized_blocks_2_sanitized_content()
        self.content_2_lines()
        temp_list = []
        for line in self.lines:
            temp_list.append(line)
            temp_list.append('\n')
        self.lines = temp_list[:-1]

        for line in self.lines:
            self.render_line(line)

    def render_line(self, line):
        '''Adds the parsed line to the textarea.
        
        Arguments:
            line (str): An unparsed string which is to be rendered to screen.

        Returns:
            None

        '''

        if line=='\n':
            self.textarea.insert(END, '\n')
        else:
            line = self.line_2_parsed_chars(line+' ')[:-1]
            if len(line)>0 and line[0].get('bulleted_list'):
                self.textarea.insert(END, '    ' + u'\u2022' + ' ')
            for char in line:
                if char.get('link'):
                    # new_file_name = os.path.join(self.app_state.base_dir, 'md', char['href'])
                    new_heading = char['href']
                    self.textarea.insert(END, char['char'], self.hyperlink.add(partial(self.app_state.show, {'screen_name':'view_screen', 'article_name': new_heading})))
                else:
                    self.textarea.insert(END, char['char'])
                attrs = [ 'bold', 'italic', 'underline', 'link', 'inline_code', 'h1', 'h2', 'bulleted_list' ]
                # attrs = attrs[:3]
                char_attrs = []
                for attr in attrs:
                    if char.get(attr):
                        char_attrs.append(attr)
                self.textarea.tag_add(self.create_tag(char_attrs), 'end -2 chars', 'end -1 chars') 

    def render(self):
        '''Renders the complete content.
        
        Arguments:
            content (str): An unparsed long string which is to be rendered to screen.

        Returns:
            None

        '''

        self.render_content()
                              

