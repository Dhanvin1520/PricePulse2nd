import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('prices.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            price REAL,
            url TEXT,
            timestamp DATETIME
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            target_price REAL,
            email TEXT,
            alerted BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_price(product_name, price, url):
    conn = sqlite3.connect('prices.db')
    c = conn.cursor()
    c.execute('INSERT INTO prices (product_name, price, url, timestamp) VALUES (?, ?, ?, ?)',
              (product_name, price, url, datetime.now()))
    conn.commit()
    conn.close()

def get_prices(url):
    conn = sqlite3.connect('prices.db')
    c = conn.cursor()
    c.execute('SELECT price, timestamp FROM prices WHERE url = ? ORDER BY timestamp', (url,))
    prices = [{'price': row[0], 'timestamp': row[1]} for row in c.fetchall()]
    conn.close()
    return prices

def add_alert(url, target_price, email):
    conn = sqlite3.connect('prices.db')
    c = conn.cursor()
    c.execute('INSERT INTO alerts (url, target_price, email) VALUES (?, ?, ?)',
              (url, target_price, email))
    conn.commit()
    conn.close()

def check_alerts(url, current_price):
    conn = sqlite3.connect('prices.db')
    c = conn.cursor()
    c.execute('SELECT id, target_price, email FROM alerts WHERE url = ? AND alerted = 0', (url,))
    alerts = c.fetchall()
    for alert in alerts:
        alert_id, target_price, email = alert
        if current_price <= target_price:
            from send_email import send_price_alert
            send_price_alert(email, "Product", current_price, target_price, url)
            c.execute('UPDATE alerts SET alerted = 1 WHERE id = ?', (alert_id,))
    conn.commit()
    conn.close()