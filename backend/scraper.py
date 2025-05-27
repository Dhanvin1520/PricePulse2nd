from playwright.sync_api import sync_playwright

def scrape_amazon(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            
            # Extract product name
            name = page.query_selector('span#productTitle').inner_text().strip()
            
            # Extract price
            price_element = page.query_selector('span.a-price-whole')
            price = float(price_element.inner_text().replace(',', '')) if price_element else 0.0
            
            # Extract image
            image = page.query_selector('img#landingImage').get_attribute('src')
            
            browser.close()
            return {
                'success': True,
                'name': name,
                'price': price,
                'image': image
            }
    except Exception as e:
        return {'success': False, 'error': str(e)}