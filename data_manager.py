from datetime import datetime
import os 

BASE_DIR = os.getcwd()

def random_id():
    now = str(datetime.now())
    now = now.replace(':', '').replace(' ', '')
    return str(now)

def create_and_save(file_name, file_content):
    path = os.path.join(BASE_DIR, 'data', 'mds', file_name+'.md')
    with open(path, 'w') as f:
        f.write(file_content)

def get_articles_list():
    path = os.path.join(BASE_DIR, 'data', 'mds')
    return os.listdir(path)

def get(file_name, file_content):
    path = os.path.join(BASE_DIR, 'data', 'mds', file_name+'.md')
    with open(path, 'r') as f:
        return f.read()

def delete(file_name):
    path = os.path.join(BASE_DIR, 'data', 'mds', file_name+'.md')
    dst = os.path.join(BASE_DIR, 'data', 'removed_mds', file_name+random_id()+'.md')
    os.rename(path, dst)

def edit(file_name, file_content):
    delete(file_name)
    create_and_save(file_name, file_content)

def check_data(file_name, file_content, action='create'):
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