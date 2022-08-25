from abc import ABC, abstractmethod
import re 

class StringParser(ABC):

    def __init__(self, chars, pattern):
        self.chars = []
        for char in chars:
            self.chars.append(char)
        self.pattern = pattern

    # remove char at i
    def remove_char_at(self, i):
        '''
        0 1 2 3 4 5 6 7 8 9
        to remove char at 5th pos, chars[:5] + char[5+1:]
        '''
        temp = self.chars[:i] + self.chars[i+1:]
        self.chars = []
        self.chars = temp 
    
    # list of chars to string
    def to_string(self):
        string = ''
        for char in self.chars:
            string = string + char['char']
        return string 

    # Find the interval matching with the pattern
    def find_matches(self):        
        regex = re.compile(self.pattern)
        return regex.findall(self.to_string())

    # strip the matched portion [opened_at, closed_at) and modify the chars
    @abstractmethod
    def modify(self, match):
        pass 

    def parse(self):
        matches = self.find_matches()
        self.modify(matches)
                
class Parser4Bold(StringParser):
    def __init__(self, string, pattern=r'\*\*[^\s].*?[^\s]\*\*[^\*]'):
        super().__init__(string, pattern)
        self.parse()
        
    # replace the chars of the bolded portion 
    def modify(self, matches):
        intervals = []
        for match in matches:
            opened_at = self.to_string().find(match)
            closed_at = opened_at + len(match) - 1
            intervals.append([closed_at, opened_at, match])
            for i in range(opened_at, closed_at):
                self.chars[i]['bold'] = True 

        intervals.sort(key=lambda x : x[0], reverse=True)
        for interval in intervals:
            closed_at = interval[0]
            opened_at = interval[1]
            self.remove_char_at(closed_at-2)
            self.remove_char_at(closed_at-2)
            self.remove_char_at(opened_at)
            self.remove_char_at(opened_at)

class Parser4Italic(StringParser):
    def __init__(self, chars, pattern=r'\*[^\s].*?[^\s]\*[^\*]'):
        super().__init__(chars, pattern)
        self.parse()
        
    # replace the chars of the italiced portion 
    def modify(self, matches):
        intervals = []
        for match in matches:
            opened_at = self.to_string().find(match)
            closed_at = opened_at + len(match) - 1
            intervals.append([closed_at, opened_at, match])
            for i in range(opened_at, closed_at):
                self.chars[i]['italic'] = True 

        intervals.sort(key=lambda x : x[0], reverse=True)
        for interval in intervals:
            closed_at = interval[0]
            opened_at = interval[1]
            self.remove_char_at(closed_at-1)
            self.remove_char_at(opened_at)

class Parser4Underline(StringParser):
    def __init__(self, chars, pattern=r'_[^\s].*?[^\s]_[^_]'):
        super().__init__(chars, pattern)
        self.parse()
        
    # replace the chars of the underlined portion 
    def modify(self, matches):
        intervals = []
        for match in matches:
            opened_at = self.to_string().find(match)
            closed_at = opened_at + len(match) - 1
            intervals.append([closed_at, opened_at, match])
            for i in range(opened_at, closed_at):
                self.chars[i]['underline'] = True 

        intervals.sort(key=lambda x : x[0], reverse=True)
        # print()
        for interval in intervals:
            closed_at = interval[0]
            opened_at = interval[1]
            self.remove_char_at(closed_at-1)
            self.remove_char_at(opened_at)

class Parser4InlineCode(StringParser):
    def __init__(self, chars, pattern=r'`[^\s].*?[^\s]`[^`]'):
        super().__init__(chars, pattern)
        self.parse()
        
    # replace the chars of the underlined portion 
    def modify(self, matches):
        intervals = []
        for match in matches:
            opened_at = self.to_string().find(match)
            closed_at = opened_at + len(match) - 1
            intervals.append([closed_at, opened_at, match])
            for i in range(opened_at, closed_at):
                self.chars[i]['inline_code'] = True 

        intervals.sort(key=lambda x : x[0], reverse=True)
        for interval in intervals:
            closed_at = interval[0]
            opened_at = interval[1]
            self.remove_char_at(closed_at-1)
            self.remove_char_at(opened_at)

class Parser4Heading1(StringParser):
    def __init__(self, chars, pattern=r'^# '):
        super().__init__(chars, pattern)
        self.parse()
        
    # replace the chars of the underlined portion 
    def modify(self, matches):
        if matches:
            match = matches[0]
            for char in self.chars:
                char['h1'] = True 
            self.remove_char_at(0)
            self.remove_char_at(0)

class Parser4Heading2(StringParser):
    def __init__(self, chars, pattern=r'^## '):
        super().__init__(chars, pattern)
        self.parse()
        
    # replace the chars of the underlined portion 
    def modify(self, matches):
        if matches:
            match = matches[0]
            for char in self.chars:
                char['h2'] = True 
            self.remove_char_at(0)
            self.remove_char_at(0)
            self.remove_char_at(0)

class Parser4BulletedList(StringParser):
    def __init__(self, chars, pattern=r'^\* '):
        super().__init__(chars, pattern)
        self.parse()
        
    # replace the chars of the underlined portion 
    def modify(self, matches):
        if matches:
            match = matches[0]
            for char in self.chars:
                char['bulleted_list'] = True 
            self.remove_char_at(0)
            self.remove_char_at(0)

class Parser4Link(StringParser):
    def __init__(self, chars, pattern=r'\[.*?\]\(.*?\)'):
        super().__init__(chars, pattern)
        self.parse()
        
    # replace the chars of the underlined portion 
    def modify(self, matches):
        intervals = []
        for match in matches:
            regex_text = re.compile(r'\[.*?\]\(')
            regex_link = re.compile(r'\]\(.*?\) ')
            text = regex_text.findall(match+' ')[0][1:-2]
            link = regex_link.findall(match+' ')[0][2:-2]

            opened_at = self.to_string().find(match)
            closed_at = opened_at + len(match) - 1
            
            text_opened_at = match.find(text) + opened_at
            text_closed_at = text_opened_at + len(text) - 1 

            link_opened_at = match.find(link) + opened_at
            link_closed_at = link_opened_at + len(link) - 1

            intervals.append([text_closed_at, len(link), text_opened_at ])

            for i in range(text_opened_at, text_closed_at+1):
                self.chars[i]['link'] = True 
                self.chars[i]['href'] = link 

            # print(f'Match {match} : ({opened_at}, {closed_at})')
            # print(f'Text {text} : ({text_opened_at}, {text_closed_at})')
            # print(f'Link {link} : ({link_opened_at}, {link_closed_at})')
        
        intervals.sort(key=lambda x: x[0], reverse=True)
        for interval in intervals:
            text_closed_at = interval[0]
            link_length = interval[1]
            text_opened_at = interval[2]

            for _ in range(text_closed_at+1, text_closed_at+link_length+4):
                self.remove_char_at(text_closed_at+1)
            
            self.remove_char_at(text_opened_at-1)

class InlineParsers():
    def __init__(self, string):
        self.list_of_parsers = []
        self.chars = self.__to_chars(string)

      
    def __to_chars(self, string):
        chars = []
        for char in string:
            chars.append({'char': char})
        return chars

    def add_parser(self, parser):
        self.list_of_parsers.append(parser)

    def parse(self):
        for parser in self.list_of_parsers:
            temp = parser(self.chars)
            self.chars = temp.chars
        return self.chars

    def pretty_print(self, chars, i=0):
        for index, char in enumerate(chars):
            print(f'{index+i:>2} |', end='')
        print()
        for char in chars:
            print(f" {char['char']} |", end='')
        print()
        for char in chars:
            if(char.get('bold')):
                print(' b |', end='')
            else:
                print('   |', end='')
        print()
        for char in chars:
            if(char.get('italic')):
                print(' i |', end='')
            else:
                print('   |', end='')
        print()
        for char in chars:
            if(char.get('underline')):
                print(' u |', end='')
            else:
                print('   |', end='')
        print()
        for char in chars:
            if(char.get('inline_code')):
                print(' c |', end='')
            else:
                print('   |', end='')
        print()
        for char in chars:
            if(char.get('h1')):
                print(' 1 |', end='')
            else:
                print('   |', end='')
        print()
        for char in chars:
            if(char.get('h2')):
                print(' 2 |', end='')
            else:
                print('   |', end='')
        print()
        for char in chars:
            if(char.get('link')):
                print(' l |', end='')
            else:
                print('   |', end='')
        print()
        for char in chars:
            if(char.get('bulleted_list')):
                print(' t |', end='')
            else:
                print('   |', end='')
        print()

    def make_pretty_print(self, length=20):
        for i in range(0, len(self.chars), length):
            self.pretty_print(self.chars[i: i+length], i)
            print()

def parse(string):
    inline_parsers = InlineParsers(string)
    parsers = [Parser4Bold, Parser4Italic, Parser4Underline, Parser4InlineCode, Parser4Heading1, Parser4Heading2, Parser4BulletedList, Parser4Link]
    for parser in parsers:
        inline_parsers.add_parser(parser)
    parsed_chars = inline_parsers.parse()
    return parsed_chars


