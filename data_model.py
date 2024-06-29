import sqlite3, math, base64, os
from werkzeug.security import generate_password_hash, check_password_hash


DBFILENAME = 'services.sqlite'

# Utility functions
def db_fetch(query, args=(), all=False, db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    # to allow access to columns by name in res
    conn.row_factory = sqlite3.Row 
    cur = conn.execute(query, args)
    # convert to a python dictionary for convenience
    if all:
      res = cur.fetchall()
      if res:
        res = [dict(e) for e in res]
      else:
        res = []
    else:
      res = cur.fetchone()
      if res:
        res = dict(res)
  return res

def db_insert(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()
    return cur.lastrowid


def db_run(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()


def db_update(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()
    return cur.rowcount

def get_services():
  res = db_fetch("SELECT * FROM service",all=True)
  return res

def get_service(id=-1, username='',all=False):
  if not(username ==''):
    res = db_fetch("SELECT * FROM service WHERE username = ?",(username,),all=all)
  if not(id == -1):
    res = db_fetch("SELECT * FROM service WHERE id = ?",(id,))
  if res:
    return res
  return None

def create_service(username, title, description, price, category, date, image):
  res = db_insert('INSERT INTO service (username, title, description, price, category, date, image) VALUES(?,?,?,?,?,?,?)',
                  (username, title, description, price, category, date, image))
  return res

def update_service(id, title, description, price, category):
  res = get_service(id)
  if (res is not None):  
    result = db_update('UPDATE service SET title = ?, description = ?, price = ?, category = ? WHERE id = ?',
                     (title, description, price, category, id))
    return True
  return False

def delete_service(id):
  res = get_service(id)
  if (res is not None):  
    result = db_update('DELETE FROM service WHERE id = ?',(id,))
    return True
  return False

def search_services(query="", page=1):
    num_per_page = 32
    res = db_fetch('SELECT count(*) FROM service WHERE title LIKE ?',
                   ('%' + query + '%',))
    num_found = res['count(*)']
    results = db_fetch('SELECT id, title, price, category, image FROM service WHERE title LIKE ? OR description LIKE ? ORDER BY id LIMIT ? OFFSET ?',
                       ('%' + query + '%', '%' + query + '%', num_per_page, (page - 1) * num_per_page), all=True)
    return {
        'results': results,
        'num_found': num_found,
        'query': query,
        'next_page': page + 1,
        'page': page,
        'num_pages': math.ceil(float(num_found) / float(num_per_page))
    }

def get_clients():
  res = db_fetch("SELECT * FROM client",all=True)
  return res

def get_client(id=-1, username='', all=False):
  if not(username ==''): 
    res = db_fetch("SELECT * FROM client WHERE username = ?", (username,), all=all)
  if not(id == -1):
    res = db_fetch("SELECT * FROM client WHERE id = ?",(id,))
  if res:
    return res
  return None

def create_client(username, title, description, price, category, date, image):
  res = db_insert('INSERT INTO client (username, title, description, price, category, date, image) VALUES(?,?,?,?,?,?,?)',
                  (username, title, description, price, category, date, image))
  return res

def update_client(id, title, description, price, category):
  res = get_client(id)
  if (res is not None):  
    result = db_update('UPDATE client SET title = ?, description = ?, price = ?, category = ? WHERE id = ?',
                     (title, description, price, category, id))
    return True
  return False

def delete_client(id):
  res = get_client(id)
  if (res is not None):  
    result = db_update('DELETE FROM client WHERE id = ?',(id,))
    return True
  return False

def search_clients(query="", page=1):
    num_per_page = 32
    res = db_fetch('SELECT count(*) FROM client WHERE title LIKE ?',
                   ('%' + query + '%',))
    num_found = res['count(*)']
    results = db_fetch('SELECT id, title, price, category, image FROM client WHERE title LIKE ? OR description LIKE ? ORDER BY id LIMIT ? OFFSET ?',
                       ('%' + query + '%', '%' + query + '%', num_per_page, (page - 1) * num_per_page), all=True)
    return {
        'results': results,
        'num_found': num_found,
        'query': query,
        'next_page': page + 1,
        'page': page,
        'num_pages': math.ceil(float(num_found) / float(num_per_page))
    }

def get_users():
  res = db_fetch("SELECT * FROM user ", all=True)
  return res


def get_user(id=-1, username='', all=False):
  if not(username ==''): 
    res = db_fetch("SELECT * FROM user WHERE username = ?", (username,), all=all)
  if not(id == -1):
    res = db_fetch("SELECT * FROM user WHERE id = ?",(id,))
  if res:
    return res
  return None

def username_exist(username):
  res = db_fetch("SELECT id FROM user WHERE username = ?",(username,))
  if res:
    return True
  return False

def login(username, password):
    res = db_fetch('SELECT id, password_hash FROM user WHERE username = ?', (username,))
    if res:
        hashed_password = res['password_hash']
        if check_password_hash(hashed_password, password):
            return res['id']
    return -1

def new_user(username, first_name, last_name, email, phone,image, password):
  if username_exist(username):
    return -1
  password_hash = generate_password_hash(password)
  res = db_insert('INSERT INTO user (username, first_name, last_name, email, phone, image, password_hash) VALUES (?,?,?,?,?,?,?)',
                        (username, first_name, last_name, email,phone,image, password_hash))
  return res

def update_user(id ,username, first_name, last_name, email, phone):
  res = get_user(id)
  if (res is not None):  
    result = db_update('UPDATE user SET username = ?, first_name = ?, last_name = ?, email = ?, phone = ? WHERE id = ?',
                     (username, first_name, last_name, email, phone, id))
    return True
  return False

def delete_account(id, password):
  res = get_user(id)
  hashed_password = res['password_hash']
  if check_password_hash(hashed_password, password):
    result = db_update('DELETE FROM user WHERE id = ?',(id,))
    return True
  return False

def update_profile_image(id, image):
  res = db_update('UPDATE user SET image = ? WHERE id= ?',(image, id))
  return res

def update_service_image(id, image):
  res = db_update('UPDATE service SET image = ? WHERE id= ?',(image, id))
  return res

def update_client_image(id, image):
  res = db_update('UPDATE client SET image = ? WHERE id= ?',(image, id))
  return res

def handle_image(request_form, image_name):
  image_data = request_form['image'].read() if 'image' in request_form else None
  if (image_data is None) or (image_data == b''):
      default_image_path = os.path.join('./static/images', image_name)
      with open(default_image_path, 'rb') as f:
            image_data = f.read()
  return image_data

def encoded_image(array=[], image=''):
    if image:
        encoded_image = base64.b64encode(image).decode('utf-8')
        return encoded_image
    
    if not array:
        return array
    
    encoded_array = []
    for res in array:
        if 'image' in res and res['image']:
            encoded_image = base64.b64encode(res['image']).decode('utf-8')
            res['image'] = encoded_image
        encoded_array.append(res)
        
    return encoded_array

def get_categories():
  res = db_fetch('SELECT * FROM category',all=True)
  return res
 
def add_category(category):
  existing_category = db_fetch('SELECT * FROM category WHERE category = ?', 
                               (category,))
  if existing_category:
    return -1
  res = db_insert('INSERT INTO category (category) VALUES (?)',
                  (category,))
  return res