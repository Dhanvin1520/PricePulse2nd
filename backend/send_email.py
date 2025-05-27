from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

def send_price_alert(to_email, product_name, current_price, target_price, url):
    message = Mail(
        from_email='dhanvin.699@gmail.com',  # Replace with your verified SendGrid sender email
        to_emails=to_email,
        subject=f'Price Drop Alert for {product_name}',
        html_content=f'''
        <h2>Price Drop Alert!</h2>
        <p>The price of {product_name} has dropped to ₹{current_price} (below your target of ₹{target_price}).</p>
        <p><a href="{url}">View Product</a></p>
        '''
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(message)
    except Exception as e:
        print(f"Email sending failed: {str(e)}")