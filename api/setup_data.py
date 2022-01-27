table_providers = '''
CREATE TABLE providers (
    id TEXT PRIMARY KEY UNIQUE,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
'''

table_collectors = '''
CREATE TABLE collectors (
    id TEXT PRIMARY KEY UNIQUE,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    quantity REAL
);
'''

table_purchases = '''
CREATE TABLE purchases (
    id TEXT PRIMARY KEY UNIQUE,
    date TEXT NOT NULL,
    price REAL NOT NULL,
    quantity REAL,
    id_provider TEXT NOT NULL,
    id_collector TEXT NOT NULL,
    FOREIGN KEY(id_provider) REFERENCES providers(id),
    FOREIGN KEY(id_collector) REFERENCES collectors(id)
);
'''

tables = (table_collectors, table_providers, table_purchases)

mock_data = {
    'collectors': [
        {'name':'Yoe', 'email': 'yoe@email.com'},
        {'name':'Arancha', 'email': 'arancha@email.com'},
        {'name':'Enrique', 'email': 'enrique@email.com'},
    ],
    'providers': [
        {'name':'Vito', 'email': 'vito@email.com'},
        {'name':'Dannel', 'email': 'dannel@email.com'},
        {'name':'Daniel', 'email': 'daniel@email.com'},
    ]
}

if __name__ == '__main__':
    import sqlite3
    import os
    from helpers import save_execute, new

    cwd = os.path.dirname(__file__)
    DB = 'honey.db'
    DBpath = os.path.join(cwd, DB)

    conn = sqlite3.connect(DBpath)

    tables_names = save_execute(
        conn,
        'SELECT name FROM sqlite_master WHERE type="table" AND name NOT LIKE "sqlite_%"',
        changes=False
        ).fetchall()
    tables_names = (table[0] for table in tables_names)
    # Drop all tables
    for table in tables_names:
        save_execute(conn, f'DROP TABLE {table}')

    # Create all tables again
    for table in tables:
        save_execute(conn, table)

    # Populate tables
    for table, rows in mock_data.items():
        for row in rows:
            new(conn, table, **row)
    conn.close()
