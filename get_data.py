import wikipediaapi
import sqlite3
import os
import sys

def get_links(page):
    links = page.links
    return links.keys()


def add_links_entry(name:str, related_items:list, database):
    cursor = database.cursor()
    # Insert the links item if it does not already exist
    cursor.execute('INSERT OR IGNORE INTO links (name) VALUES (?)', (name,))
    
    # Get the id of the inserted or existing links item
    cursor.execute('SELECT id FROM links WHERE name = ?', (name,))
    links_id = cursor.fetchone()[0]
    
    for related_name in related_items:
        # Insert the related links item if it does not already exist
        cursor.execute('INSERT OR IGNORE INTO links (name) VALUES (?)', (related_name,))
        
        # Get the id of the related links item
        cursor.execute('SELECT id FROM links WHERE name = ?', (related_name,))
        related_id = cursor.fetchone()[0]
        
        # Insert the relationship if it does not already exist
        cursor.execute('''
        INSERT OR IGNORE INTO related_links (links_id, related_id)
        VALUES (?, ?)
        ''', (links_id, related_id))

    # Commit changes to the database
    database.commit()
    cursor.close()


def get_list(category):
    os.remove('links.db')


    wiki_wiki = wikipediaapi.Wikipedia(user_agent='MyProjectName (merlin@example.com)', language='en')
    
    database = sqlite3.connect('links.db')

    cursor = database.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS related_links (
        id INTEGER PRIMARY KEY,
        links_id INTEGER,
        related_id INTEGER,
        FOREIGN KEY (links_id) REFERENCES links(id),
        FOREIGN KEY (related_id) REFERENCES links(id)
    )
    ''')



    database.commit()

    # for i in range(1000):
    #     cursor.execute('SELECT * FROM related_links')
    #     raw_list = cursor.fetchall()
    #     try:
    #         name = cursor.execute('SELECT name FROM Links WHERE id = ?', (raw_list[-1][2],)).fetchone()[0]
    #     except IndexError:
    #         print('INDEX ERROR')
    #         name = 'Python_(programming_language)'
    #     page = wiki_wiki.page(name)
    #     add_links_entry(name, get_links(page), database)

    category = category.replace(' ', '_')

    start = wiki_wiki.page(category)

    keys = start.categorymembers.keys()
    keys = [page for page in keys if not page.startswith('Category:')]
    
    for name in keys:
        add_links_entry(name, get_links(wiki_wiki.page(name)), database)

        
    cursor.close()
    database.close()

def get_clean_info():
    database = sqlite3.connect('links.db')

    cursor = database.cursor()

    cursor.execute('SELECT * FROM related_links')
    raw_list = cursor.fetchall()

    compiled_list = []

    for tup in raw_list:
        compiled_list.append(
            (
                (cursor.execute('SELECT name FROM Links WHERE id = ?', (tup[1],)).fetchone()[0]),
                (cursor.execute('SELECT name FROM Links WHERE id = ?', (tup[2],)).fetchone()[0])
            )
        )
    
    return compiled_list


if __name__ == '__main__':
    get_list(sys.argv[1])