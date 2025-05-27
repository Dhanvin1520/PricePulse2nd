from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_amazon
from database import add_price, check_alerts

def schedule_price_check():
    from app import app
    with app.app_context():
        conn = sqlite3.connect('prices.db')
        c = conn.cursor()
        c.execute('SELECT DISTINCT url FROM prices')
        urls = [row[0] for row in c.fetchall()]
        conn.close()
        
        for url in urls:
            product_data = scrape_amazon(url)
            if product_data['success']:
                add_price(product_data['name'], product_data['price'], url)
                check_alerts(url, product_data['price'])

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_price_check, 'interval', minutes=30)
    scheduler.start()