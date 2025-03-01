import sqlite3

conn = sqlite3.connect('database.db')

print("Connected to database successfully")

# conn.execute('CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, created_at DATE)')

# conn.execute('INSERT INTO users (name, email, created_at) VALUES ("majk", "majk@gmail.com", "2025-02-25 14:35:12")')

# cur.execute('INSERT INTO users (name) VALUES ("Alice"), ("Bob"), ("Mike")')

# cur.execute('INSERT INTO user_activity (user_id, login_date) VALUES (2, "2025-02-25")')

# conn.execute('CREATE TABLE user_activity (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, login_date DATE, FOREIGN KEY (user_id) REFERENCES users(id))')

# conn.execute('CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price FLOAT NOT NULL)')

# conn.execute('CREATE TABLE purchases (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, total_price FLOAT NOT NULL, purchase_date DATE, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (product_id) REFERENCES products(id))')

# cur.execute('INSERT INTO products (name, price) VALUES ("Laptop", 1200.99), ("Smartphone", 799.49), ("Headphones", 199.99), ("Gaming Mouse", 49.99), ("Mechanical Keyboard", 129.99), ("Smartwatch", 249.99), ("External SSD", 99.99), ("Wireless Charger", 39.99)')

# cur.execute('SELECT login_date FROM users JOIN user_activity ON users.id = user_activity.user_id WHERE user_activity.user_id = 2')

# cur.execute('INSERT INTO users (name, created_at) VALUES ("alice", "2025-02-28")')

# cur.execute('delete from user_activity where user_id = 1')

# cur.execute('INSERT INTO purchases (user_id, product_id, quantity, total_price, purchase_date) VALUES(2, 2, 1, 799.49, "2025-02-07"),(2, 5, 1, 129.99, "2025-02-10"),(3, 4, 2, 99.98, "2025-02-12"),(3, 7, 1, 99.99, "2025-02-15"),(4, 6, 1, 249.99, "2025-02-18"),(4, 8, 3, 119.97, "2025-02-20"),(5, 1, 1, 1200.99, "2025-02-22"),(5, 2, 1, 799.49, "2025-02-25")')

print("Created table successfully!")

conn.close()