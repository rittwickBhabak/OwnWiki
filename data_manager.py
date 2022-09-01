'''This modules handles all of the read and writes from the database.

Currently all the articles are residing inside a directory inside the app.
But later it can be easily integrated to some cloud database.

'''

from datetime import datetime
import os 

BASE_DIR = os.getcwd()

def random_id():
    '''Generates a random id from the current time.'''

    now = str(datetime.now())
    now = now.replace(':', '').replace(' ', '')
    return str(now)

def create_and_save(file_name, file_content):
    '''Creates a new article and saves it to directory.
    
    Arguments:
        file_name (str): article name
        
        file_content (str): article content 
    Returns:
        None
    
    '''
    
    path = os.path.join(BASE_DIR, 'data', 'mds', file_name+'.md')
    with open(path, 'w') as f:
        f.write(file_content)

def get_articles_list():
    '''Scans over the database and finds all of the article names.
    
    Arguments:
        None 
    
    Return:
        list of article names
    
    '''
    
    path = os.path.join(BASE_DIR, 'data', 'mds')
    return os.listdir(path)

def get(file_name):
    '''Reads the article content.
    
    Arguments:
        file_name (str): article name 
    
    Returns:
        returns a string containing article content.
        
    '''
    
    path = os.path.join(BASE_DIR, 'data', 'mds', file_name+'.md')
    with open(path, 'r') as f:
        return f.read()

def delete(file_name):
    '''Deletes an article from the database.
    
    Arguments:
        file_name (str): article name
    
    Returns:
        None 
    
    '''

    path = os.path.join(BASE_DIR, 'data', 'mds', file_name+'.md')
    dst = os.path.join(BASE_DIR, 'data', 'removed_mds', file_name+random_id()+'.md')
    os.rename(path, dst)

def edit(file_name, file_content):
    '''Edits an article in the database.
    
    Arguments:
        file_name (str): article name
    
    Returns:
        None 
    
    '''
    
    delete(file_name)
    create_and_save(file_name, file_content)

def check_data(file_name, file_content, action='create'):
    '''Checks that if create and save or edit and save can be performed.

    If an article already exists then this asks the user if user still wants\
        to save the file or continue to edit the existing file.
    If the article name is passed blank then it does not allow user to save it.
    If the article content is passed blank then it confirms form the user \
        if user still wants to save the article with no content.
    
    Arguments:
        file_name (str): article name
        file_content (str): article content
        action (str): namely the mode of action like 'create'(default) or 'edit'
    
    Returns:
        None 
    
    '''
    
    if file_name.strip()=='':
        return {
            'code': 1,
            'message': 'Article Name cannot be blank',
        }
    all_articles = list(map(lambda x:x[:-3].lower(), get_articles_list()))
    if action=='create' and file_name.lower() in all_articles:
        return {
            'code': 2,
            'message': 'An article with the same name already exists. Do you still want to overwrite the existing article(yes) or edit the existing article?(no)',
        }
    if file_content.strip()=='':
        return {
            'code': 3,
            'message': 'The article content is blank. Do you still want to save it?',
        }
    return {
        'code': 4
    }