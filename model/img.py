import data_model as model
import os
from werkzeug.utils import secure_filename

def save_image_to_db(filename):
    res = model.db_insert('INSERT INTO images (filename) VALUES (?)', (filename,))
    return res

def upload_image(image,folder):
    if image.filename != '':
        filename = secure_filename(image.filename)
        image.save(os.path.join(folder, filename))
        save_image_to_db(filename)
        return True
    return False