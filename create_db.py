import sqlite3

DBFILENAME = 'services.sqlite'

categories = [
    "Social Media Management",
    "Search Engine Optimization (SEO)",
    "Pay-Per-Click Advertising (PPC)",
    "Email Marketing",
    "Video Production and Editing",
    "Web Analytics",
    "E-commerce Development",
    "App Development",
    "UI/UX Design",
    "Copywriting",
    "Blogging",
    "Influencer Marketing",
    "Podcast Production",
    "Affiliate Marketing",
    "Online Reputation Management",
    "Conversion Rate Optimization (CRO)",
    "Lead Generation Services",
    "Mobile Marketing",
    "Online PR Services",
    "Virtual Event Planning"
]


def db_run(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()

def create():
  db_run('CREATE TABLE IF NOT EXISTS service (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, title TEXT, description TEXT, price REAL, category TEXT, date TEXT, image BLOB)')
  db_run('CREATE TABLE IF NOT EXISTS client (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, title TEXT, description TEXT, price REAL, category TEXT, date TEXT, image BLOB)')
  db_run('CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT)')
  
  db_run('''CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            first_name TEXT,
            last_name TEXT,
            email TEXT ,
            phone TEXT,
            image BLOB,
            password_hash TEXT)''')

db_run('DELETE FROM service')