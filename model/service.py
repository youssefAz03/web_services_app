import data_model as model

def get_services():
  res = model.db_fetch("SELECT * FROM service",all=True)
  return res

def get_service(id):
  res = model.db_fetch("SELECT * FROM service WHERE id = ?",(id,))
  if res:
    return res
  return None

def create_service(username, title, description, price, category, img):
  res = model.db_insert('INSERT INTO service (username, title, description, price, category, img) VALUES(?,?,?,?,?,?)',
                  (username, title, description, price, category, img))
  return res

def update_service(id, title, description, price, category, img):
  res = get_service(id)
  if (res is not None):  
    result = model.db_update('UPDATE service SET title = ?, description = ?, price = ?, category = ?, img = ? WHERE id = ?',
                     (title, description, price, category, img, id))
    return True
  return False

def delete_service(id):
  res = get_service(id)
  if (res is not None):  
    result = model.db_update('DELETE FROM service WHERE id = ?',(id,))
    return True
  return False
