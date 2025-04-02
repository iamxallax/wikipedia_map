import wikipediaapi
import sqlite3

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


def main():
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='MyProjectName (merlin@example.com)', language='en')

    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    title = url.split('/wiki/')[-1]

    page = wiki_wiki.page(title)

    if page.exists():
        print(f"Title: {page.title}")
        print(get_links(page))
    else:
        print("Page does not exist.")
    
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

    add_links_entry('Python_(programming_language)', get_links(page), database)

    cursor.execute('SELECT * FROM related_links')
    raw_list = cursor.fetchall()


    compiled_list = []
    for tup in raw_list:
        compiled_list.append(
            (
                (tup[1], cursor.execute('SELECT name FROM Links WHERE id = ?', (tup[1],)).fetchone()[0]),
                (tup[2], cursor.execute('SELECT name FROM Links WHERE id = ?', (tup[2],)).fetchone()[0])
            )
        )

    cursor.close()
    database.close()
    
    
    return compiled_list
                                                        
