import faiss
import constant
import os

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
			distances,indices=SearchClass._cached_index.search(vector,10)
			return indices
		except Exception as e:
			print(e)