import os
import sqlite3
import hashlib
from PIL import Image
import torch
from pillow_heif import register_heif_opener

register_heif_opener()

db_name = "processed.db"

def verify_image(path):
    try:
        img = Image.open(path)
        img.verify()
        return True
    except (IOError) as e:
        #print(f'invalid file : {path}, error : {e}')
        return False
    except Exception as e:
        #print('Error unknown : {e}')
        return False

def image_path_gen(path):
    image_paths = []
    for segment in os.listdir(path):
        image_path = os.path.join(path,segment)
        if verify_image(image_path):
            image_paths.append(image_path)

    return image_paths

"""
def path_code_gen(image_paths):
    codes = [hasher(image_path) for image_path in image_paths]
    return codes
"""

def hasher(path_string):
    return hashlib.md5(path_string.encode()).hexdigest()


from itertools import batched
from image_descriptor import describe
from appender import write_finder_comment

def manager_func(path,processor,model):
    db_path = os.path.join(path, db_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS processedImages (
        Id TEXT PRIMARY KEY,
        hashCode TEXT NOT NULL
    )
    """)
    conn.commit()

    db_code = c.execute("SELECT hashCode FROM processedImages")
    db_code = list(db_code.fetchall())

    list_of_strings = []
    for item in db_code:
        for string in item:
            list_of_strings.append(string)

    image_paths = image_path_gen(path)

    unprocessed_imgs = []

    for image_path in image_paths:
        img_code = hasher(image_path)
        if img_code in list_of_strings:
            print(f'already processed: {image_path}')
            continue
        else:
            unprocessed_imgs.append(image_path)
    
    if unprocessed_imgs:
        batch_size = 5
        i = 0
        for batch in batched(unprocessed_imgs,batch_size):
            data = []
            i += 1
            print(f'processing batch: {i}')
            for img_path in batch:
                try:
                    desp = describe(img_path,processor,model)
                    write_finder_comment(image_path=img_path,description=desp)
                    code = hasher(img_path)
                    data.append((img_path,code)) 
                    c.executemany("INSERT OR IGNORE INTO processedImages (Id, hashCode) VALUES (?, ?)",data)
                    conn.commit()
                except Exception as e:
                    print(f'Error: {e}')
            print(f'finished with batch: {i}')
    else:
        print('no unprocessed images')

    conn.close()

