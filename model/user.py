import data_model as model

def get_users():
  res = model.db_fetch("SELECT * FROM user ", all=True)
  return res


def get_user(id):
  res = model.db_fetch("SELECT * FROM user WHERE id = ?",(id,))
  if res:
    return res
  return None


def username_exist(username):
  res = model.db_fetch("SELECT id FROM user WHERE username = ?",(username,))
  if res:
    return True
  return False

def login(username, password):
    res = model.db_fetch('SELECT id, password_hash FROM user WHERE username = ?', (username,))
    if res:
        hashed_password = res['password_hash']
        if model.check_password_hash(hashed_password, password):
            return res['id']
    return -1

def new_user(username, first_name, last_name, email, phone, password):
  if username_exist(username):
    return -1
  password_hash = model.generate_password_hash(password)
  res = model.db_insert('INSERT INTO user (username, first_name, last_name, email, phone, password_hash) VALUES (?,?,?,?,?,?)',
                        (username, first_name, last_name, email,phone, password_hash))
  return res
