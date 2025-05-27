from flask import Flask, request, jsonify
from database import init_db, add_price, get_prices, add_alert, check_alerts
from scraper import scrape_amazon
from scheduler import start_scheduler
# Removed unused import
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/api/track', methods=['POST'])
def track_product():
    data = request.json
    url = data.get('url')
    target_price = data.get('target_price')
    email = data.get('email')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        product_data = scrape_amazon(url)
        if not product_data['success']:
            return jsonify({'error': product_data['error']}), 400

        add_price(product_data['name'], product_data['price'], url)
        
        if target_price and email:
            add_alert(url, float(target_price), email)
        
        return jsonify({
            'name': product_data['name'],
            'price': product_data['price'],
            'image': product_data['image'],
            'url': url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prices/<path:url>', methods=['GET'])
def get_price_history(url):
    prices = get_prices(url)
    return jsonify(prices)

@app.route('/api/check_alerts', methods=['POST'])
def check_price_alerts():
    data = request.json
    url = data.get('url')
    current_price = data.get('current_price')
    check_alerts(url, current_price)
    return jsonify({'status': 'checked'})

if __name__ == '__main__':
    init_db()
    start_scheduler()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5002)))