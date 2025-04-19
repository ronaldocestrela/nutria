from tinydb import table
from database.engine import Engine

class BaseRepository(Engine):
	def get_table(self, table_name: str) -> table.Table:
		"""
		Get the table from the database engine.
		"""
		return self.db.table(table_name)

	