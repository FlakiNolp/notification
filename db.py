import sqlite3


class DataBase():

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    async def add_new_user(self, source, email, telegram, vk, website):
        with self.connection:
            return self.cursor.execute('INSERT INTO users (source, email, telegram_id, vk_domen, website) VALUES (?, ?, ?, ?, ?)', (source, email, telegram, vk, website))

    async def delete_user(self, source):
        with self.connection:
            return self.cursor.execute('DELETE FROM users WHERE source = ?', (source,))

    async def edit_user(self, source, email, telegram, vk, website):
        with self.connection:
            return self.cursor.execute('UPDATE users SET email = ?, telegram_id = ?, vk_domen = ?, website = ? WHERE source = ?', (email, telegram, vk, website, source))

    async def get_all_sources(self):
        with self.connection:
            return self.cursor.execute('SELECT source FROM users').fetchall()

    async def get_user(self, source):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users WHERE source = ?', (source,)).fetchall()[0]
