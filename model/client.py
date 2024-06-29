import data_model as model

def get_clients():
  res = model.db_fetch("SELECT * FROM client",all=True)
  return res

def get_client(id):
  res = model.db_fetch("SELECT * FROM client WHERE id = ?",(id,))
  if res:
    return res
  return None

def create_client(username, title, description, price, category, img):
  res = model.db_insert('INSERT INTO client (username, title, description, price, category, img) VALUES(?,?,?,?,?,?)',
                  (username, title, description, price, category, img))
  return res

def update_client(id, title, description, price, category, img):
  res = get_client(id)
  if (res is not None):  
    result = model.db_update('UPDATE client SET title = ?, description = ?, price = ?, category = ?, img = ? WHERE id = ?',
                     (title, description, price, category, img, id))
    return True
  return False

def delete_client(id):
  res = get_client(id)
  if (res is not None):  
    result = model.db_update('DELETE FROM client WHERE id = ?',(id,))
    return True
  return False
