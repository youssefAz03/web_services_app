from flask import Flask, session, render_template, redirect, url_for, request, flash, Response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from werkzeug.utils import secure_filename
from datetime import datetime
import data_model as model
import os, base64

app = Flask(__name__)
UPLOAD_FOLDER = './static/images'  # Create an 'uploads' directory in your Flask app directory
# Ensure the 'uploads' directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = b'6dbb6b3863634aa6a72270de16df48e666f2564fddcc5fe3c27effe4393a7f4b'

########################################
# Routes des pages principales du site #
########################################
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not('username' in session):
            return Response("Accès non autorisé", status=401)
        else:
            return f(*args, **kwargs)
    return decorated_function

@app.get('/')
def home():
    services = model.get_services()
    return render_template('index.html', services = services)

##############   user routes   ################
@app.get('/login')
def login_form():
    return render_template('login.html')

@app.post('/login')
def login():
  username =  request.form['username']
  password =  request.form['password']
  id = model.login(username, password)
  if not(id == -1):
    session.clear()
    session['id'] = id
    session['username'] = username
    return redirect(url_for('home'))
  else:
    return render_template('login.html', id=id)
  
@app.get('/sign_up')
def sign_up_form():
   return render_template('sign_up.html')

@app.post('/sign_up')
def sign_up():
    username = request.form['username']
    image_data = request.files['image'].read() if 'image' in request.files else None

    id = model.new_user(request.form['username'],
                        request.form['first_name'],
                        request.form['last_name'],
                        request.form['email'],
                        request.form['phone'],
                        image_data,
                        request.form['password'])
    if id == -1:
        return render_template('sign_up.html',id =id)
    else:
        session.clear()
        session['id'] = id
        session['username'] = username
        return redirect(url_for('home'))
    
@app.post('/logout')
def logout():
   session.clear()
   return redirect(url_for('home'))

##############   profile routes   ################

@app.get('/profile/<id>')
def profile(id):
    user = model.get_user(int(id))
    user['image'] = model.encoded_image(image=user['image'])   
    clients = model.encoded_image(array=model.get_client(username=user['username'], all=True))
    services = model.encoded_image(array=model.get_service(username=user['username'], all=True))

    return render_template('profile.html', user=user, services=services, clients=clients)

@app.route('/profile')
def profile_redirect():
    if 'id' in session:
        return redirect(url_for('profile', id=session['id']))
    else:
        return redirect(url_for('login_form'))

@app.get('/update_profile')
@login_required
def update_profile_form():
    id = session['id']
    user = model.get_user(id)
    return render_template('update_profile.html',user=user)
 
@app.post('/update_profile')
@login_required
def update_profile():
    id = session['id']
    res = model.update_user(id,**request.form)
    return redirect(url_for('profile', id=str(id)))

@app.get('/update_profile_image')
@login_required
def update_profile_image_form():
  return render_template('update_profile_image.html')

@app.post('/update_profile_image')
@login_required
def update_profile_image():
  id = session['id'] 

  image_data = model.handle_image(request.files, 'user.png')
  res = model.update_profile_image(id, image_data)
  return redirect(url_for('profile', id=str(id)))

##############   service routes   ################

@app.get('/service/<id>')
def get_service(id):
  service = model.get_service(id=int(id))
  service['image'] = model.encoded_image(image=service['image'])
  user_id = model.get_user(username=service['username'])['id']
  return render_template('read_service.html',service = service, id=user_id)

@app.get('/create_service')
@login_required
def create_service_form():
  categories = model.get_categories()
  return render_template('create_service.html', categories=categories)

@app.post('/create_service')
@login_required
def create_service():
    image_data = model.handle_image(request.files, 'user.png')
    current_date = datetime.now().strftime('%Y-%m-%d')
    id = session['id']
    service_id = model.create_service(session['username'],
                        request.form['title'],
                        request.form['description'],
                        request.form['price'],
                        request.form['category'],
                        current_date,
                        image_data)
    return redirect(url_for('profile', id=str(id)))

@app.get('/delete_service/<id>')
@login_required
def delete_service_form(id):
   service = model.get_service(id=int(id))
   return render_template('delete_service.html',service=service)

@app.post('/delete_service/<id>')
@login_required
def delete_service(id):
  res = model.delete_service(id)
  return redirect(url_for('profile', id=session['id']))

@app.get('/update_service/<id>')
@login_required
def update_service_form(id):
  categories = model.get_categories()
  service = model.get_service(id=int(id))
  return render_template('update_service.html', service=service, categories=categories)

@app.post('/update_service/<id>')
@login_required
def update_service(id):
    user_id = session['id']
    res = model.update_service(int(id), **request.form)
    return redirect(url_for('profile', id=str(user_id)))

@app.get('/update_service_image/<id>')
@login_required
def update_service_image_form(id):
  service = model.get_service(id=int(id))
  return render_template('update_service_image.html',service=service)

@app.post('/update_service_image/<id>')
@login_required
def update_service_image(id): 
  image_data = model.handle_image(request.files, 'service.png')

  res = model.update_service_image(id, image_data)
  return redirect(url_for('get_service', id=str(id)))

##############   client routes   ################

@app.get('/client/<id>')
def get_client(id):
  client = model.get_client(id=int(id))
  client['image'] = model.encoded_image(image=client['image'])
  user_id = model.get_user(username=client['username'])['id']
  return render_template('read_client.html',client = client, id=user_id)

@app.get('/create_client')
@login_required
def create_client_form():
  categories = model.get_categories()
  return render_template('create_client.html', categories=categories)

@app.post('/create_client')
@login_required
def create_client():
    image_data = model.handle_image(request.files, 'client.png')
    current_date = datetime.now().strftime('%Y-%m-%d')
    id = session['id']
    client_id = model.create_client(session['username'],
                                    request.form['title'],
                                    request.form['description'],
                                    request.form['price'],
                                    request.form['category'],
                                    current_date,
                                    image_data)
    return redirect(url_for('profile', id=str(id)))

@app.get('/delete_client/<id>')
@login_required
def delete_client_form(id):
   client = model.get_client(id=int(id))
   return render_template('delete_client.html',client=client)

@app.post('/delete_client/<id>')
@login_required
def delete_client(id):
  res = model.delete_client(id)
  return redirect(url_for('profile', id=session['id']))

@app.get('/update_client/<id>')
@login_required
def update_client_form(id):
  categories = model.get_categories()
  client = model.get_client(id=int(id))
  return render_template('update_client.html', client=client, categories=categories)

@app.post('/update_client/<id>')
@login_required
def update_client(id):
    user_id = session['id']
    res = model.update_client(int(id), **request.form)
    return redirect(url_for('profile', id=str(user_id)))

@app.get('/update_client_image/<id>')
@login_required
def update_client_image_form(id):
  client = model.get_client(id=int(id))
  return render_template('update_client_image.html',client=client)

@app.post('/update_client_image/<id>')
@login_required
def update_client_image(id): 
  image_data = model.handle_image(request.files, 'service.png')

  res = model.update_client_image(id, image_data)
  return redirect(url_for('get_client', id=str(id)))

##############   search routes   ################

# @app.get('/services')
# def get_services():
#   services = model.get_services()
#   for service in services:
#     service['image'] = model.encoded_image(image=service['image'])
#   return render_template('services.html',services = services)


@app.get('/search_services')
def search_services():
  if 'page' in request.args:
    page = int(request.args["page"])   
  else:
    page = 1
  if 'query' in request.args:
    query = request.args["query"]
  else:
    query = ""
  found = model.search_services(query, page)
  for service in found['results']:
    service['image'] = model.encoded_image(image=service['image'])

  return render_template('search_services.html', found=found)

@app.get('/search_clients')
def search_clients():
  if 'page' in request.args:
    page = int(request.args["page"])   
  else:
    page = 1
  if 'query' in request.args:
    query = request.args["query"]
  else:
    query = ""
  found = model.search_clients(query, page)
  for client in found['results']:
    client['image'] = model.encoded_image(image=client['image'])

  return render_template('search_clients.html', found=found)