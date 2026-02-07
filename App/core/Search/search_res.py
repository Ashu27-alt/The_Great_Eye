import faiss
import constant
import os
import sqlite3

class SearchClass():
	_cached_index=None
	@classmethod
	def loadIndex(cls,force_reload=False):
		if cls._cached_index is None or force_reload:
			if os.path.exists(constant.INDEX_PATH):
				print('Caching index.....')
				cls._cached_index=faiss.read_index(constant.INDEX_PATH)
			else:
				print('Nothing to cache.')

	@staticmethod
	def res(vector):
		SearchClass.loadIndex()
		if SearchClass._cached_index is None:
			print('not cached.')
			return []
		
		try:
			distances,indices=SearchClass._cached_index.search(vector,20)

			conn=sqlite3.connect(constant.DB_PATH)
			c=conn.cursor()
			paths=[]

			for idx in indices[0]:
				dbId=int(idx)+1

				c.execute("SELECT image_path FROM processed WHERE Id = ?", (dbId,))
				data=c.fetchone()
				if data:
					paths.append(data[0])
			
			return paths

		except Exception as e:
			print(e)