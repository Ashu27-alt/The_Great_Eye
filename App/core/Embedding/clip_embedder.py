from PIL import Image
import os
from pillow_heif import register_heif_opener
import sqlite3
import hashlib
from itertools import batched
import torch
import faiss
import numpy as np
import constant
from core.Search.search_res import SearchClass

register_heif_opener()

class Embedder():
	@staticmethod
	def hasher(name):
		return hashlib.md5(name.encode()).hexdigest()
	
	@staticmethod
	def image_embedder(*,path,model,processor,device,progressCallback):

		db_path=constant.DB_PATH
		index_path=constant.INDEX_PATH
		dim=512

		if SearchClass._cached_index is not None:
			index=SearchClass._cached_index
		elif os.path.exists(index_path):
			index=faiss.read_index(index_path)
		else:
			index=faiss.IndexFlatIP(dim)

		conn=sqlite3.connect(db_path)
		c=conn.cursor()

		c.execute("""
		CREATE TABLE IF NOT EXISTS processed(
			Id INTEGER PRIMARY KEY,
			image_hash TEXT NOT NULL,
			image_path TEXT NOT NULL
		)
		""")

		conn.commit()

		db_code=c.execute("SELECT image_hash FROM processed")
		db_code=list(db_code.fetchall())

		image_hash={row[0] for row in db_code}

		count = 0
		images = []

		Extensions = ['.jpg','.heic','.jpeg']
		for r,d,files in os.walk(path):
			for f in files:
					if f.lower().endswith(tuple(Extensions)):
						full_path=os.path.join(r,f)
						images.append(full_path)
						count+=1
		
		if images:
			batch_size = 10
			i=1
			countp = 0
			last_percent = -1

			for batch in batched(images, batch_size):
				print(f'processing batch: {i}')
				i+=1
				db_data=[]
				batch_vectors=[]
				for image_path in batch:
					countp += 1
					img_hash=Embedder.hasher(image_path)

					if img_hash in image_hash:
							continue
					
					try:
						img=Image.open(image_path).convert("RGB")
						input = processor(images=img,return_tensors='pt').to(device)

						with torch.no_grad():
							output=model.get_image_features(**input)

						
						output=output/output.norm(dim=1,keepdim=True)
						vector=output.cpu().numpy().astype('float32')
						batch_vectors.append(vector)
						db_data.append((img_hash,image_path))
					except Exception as e:
						print(e)
				if batch_vectors:
					v_array=np.vstack(batch_vectors)
					index.add(v_array)
					c.executemany("INSERT OR IGNORE INTO processed (image_hash,image_path) VALUES (?,?)",db_data)
					conn.commit()

				per = int((countp / count) * 100)
				if per != last_percent:
					progressCallback(per)
					last_percent = per

			faiss.write_index(index,index_path)
			SearchClass._cached_index=index
			progressCallback(100)
		conn.close()

	@staticmethod      
	def text_embedder(*,query,model,processor,device):
		try:
			input=processor(text=[query],return_tensors='pt',padding=True).to(device)
			with torch.no_grad():
				vector=model.get_text_features(**input)
			vector=vector/vector.norm(dim=1,keepdim=True)
			return vector.cpu().numpy().astype('float32')
		except Exception as e:
			print(e)