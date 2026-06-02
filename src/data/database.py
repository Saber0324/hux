import aiosqlite


class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    async def setup(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                            CREATE TABLE IF NOT EXISTS snippets (
                                title TEXT UNIQUE COLLATE NOCASE,
                                description TEXT,
                                author_id INTEGER,
                                locked INTEGER DEFAULT 0)
                            """)

            await db.execute("""
                            CREATE TABLE IF NOT EXISTS warns (
                            user_id INTEGER,
                            reason TEXT,
                            moderator_id INTEGER,
                            date TEXT DEFAULT CURRENT_TIMESTAMP,
                            warn_id INTEGER PRIMARY KEY)
                            """)

            await db.execute("""
                            CREATE TABLE IF NOT EXISTS projects (
                            user_id INTEGER,
                            reason TEXT,
                            moderator_id INTEGER,
                            date TEXT DEFAULT CURRENT_TIMESTAMP,
                            warn_id INTEGER PRIMARY KEY)
                            """)

            await db.commit()

    async def insert(self, table, values):
        async with aiosqlite.connect(self.db_path) as db:
            placeholders = ", ".join("?" for _ in values)
            await db.execute(f"INSERT INTO {table} VALUES ({placeholders})", values)
            await db.commit()

    async def get_one(self, table, column, value):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                f"SELECT * FROM {table} WHERE {column} = ?", (value,)
            ) as cursor:
                return await cursor.fetchone()

    async def get_all(self, table):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(f"SELECT * FROM {table}") as cursor:
                return await cursor.fetchall()

    async def get_all_where(self, table, column, value):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                f"SELECT * FROM {table} WHERE {column} = ?", (value,)
            ) as cursor:
                return await cursor.fetchall()

    async def update(self, table, column, value, where_column, where_value):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                f"UPDATE {table} SET {column} = ? WHERE {where_column} = ?",
                (value, where_value),
            )
            await db.commit()

    async def delete(self, table, column, value):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"DELETE FROM {table} WHERE {column} = ?", (value,))
            await db.commit()
