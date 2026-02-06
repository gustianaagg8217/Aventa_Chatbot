import json
import sqlite3
import requests

class VocabularyManager:
    def __init__(self, db_name='vocabulary.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS vocabulary (
                    word TEXT PRIMARY KEY,
                    meaning TEXT
                )
            ''')

    def add_word(self, word, meaning):
        with self.connection:
            self.connection.execute('INSERT INTO vocabulary (word, meaning) VALUES (?, ?)', (word, meaning))

    def get_meaning(self, word):
        cursor = self.connection.cursor()
        cursor.execute('SELECT meaning FROM vocabulary WHERE word = ?', (word,))
        result = cursor.fetchone()
        return result[0] if result else None

    def fetch_online_meaning(self, word):
        # Replace with a real API endpoint and key
        response = requests.get(f'https://api.example.com/getMeaning?word={word}')
        if response.status_code == 200:
            return response.json().get('meaning')
        return None

    def close(self):
        self.connection.close()

# Example usage:
if __name__ == '__main__':
    vocab_manager = VocabularyManager()
    vocab_manager.add_word('example', 'a representative form or pattern')
    print(vocab_manager.get_meaning('example'))
    print(vocab_manager.fetch_online_meaning('example'))
    vocab_manager.close()