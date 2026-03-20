import sqlite3
import os

DB_NAME = "inventory.db"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "inventory.db")

class InventoryDB:
	def __init__(self, db_name=DB_NAME):
		self.db_name = db_name
		self._create_table()

	def _connect(self):
		return sqlite3.connect(self.db_name)

	def _create_table(self):
		with self._connect() as conn:
			conn.execute("""
				CREATE TABLE IF NOT EXISTS inventory (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					name TEXT NOT NULL UNIQUE,
					quantity INTEGER NOT NULL DEFAULT 0
				)
			""")
	def add_item(self, name, quantity):
		with self._connect() as conn:
			conn.execute("""
				INSERT INTO inventory (name, quantity) 
				VALUES (?, ?)
				ON CONFLICT(name) DO UPDATE SET 
				quantity = quantity + excluded.quantity
				""", (name, quantity))
			conn.commit()

	def clear_inventory(self):
		with self._connect() as conn:
			conn.execute("DELETE FROM inventory")
			conn.commit()

	def get_all_items(self):
		with self._connect() as conn:
			cursor = conn.execute("""SELECT * FROM inventory""")
			return cursor.fetchall()