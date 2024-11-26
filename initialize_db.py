import sqlite3

def initialize_database():
    with open('schema.sql', 'r') as schema_file:
        schema = schema_file.read()

    with sqlite3.connect('hw12.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(schema)
        print("Database initialized successfully.")

if __name__ == '__main__':
    initialize_database()