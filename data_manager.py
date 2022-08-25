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
    