import requests
import base64
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

def checkout(request, product_id):
    # Retrieve the selected product
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        # Base64 encode the consumer_key and consumer_secret
        consumer_key = 'YOUR_CONSUMER_KEY'
        consumer_secret = 'YOUR_CONSUMER_SECRET'
        encoded_key_secret = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

        # Generate a token to access the API
        access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        headers = {'Authorization': f'Basic {encoded_key_secret}'}
        response = requests.get(access_token_url, headers=headers)
        access_token = response.json()['access_token']

        # Make a transaction
        transaction_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        transaction_payload = {
            'BusinessShortCode': 'YOUR_SHORTCODE',
            'Password': base64.b64encode(f'{YOUR_SHORTCODE_PASSKEY}{timestamp}'.encode()).decode(),
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': str(product.price),
            'PartyA': 'YOUR_PHONE_NUMBER',
            'PartyB': 'YOUR_SHORTCODE',
            'PhoneNumber': 'YOUR_PHONE_NUMBER',
            'CallBackURL': 'https://example.com/callback',
            'AccountReference': 'YOUR_REFERENCE',
            'TransactionDesc': f'Purchase of {product.name}'
        }
        response = requests.post(transaction_url, json=transaction_payload, headers=headers)
       
        # Handle the response from the API
        # You can customize this part based on your requirements
        if response.status_code == 200:
            # Payment successful, show a success message
            return HttpResponse("Payment successful!")
        else:
            # Payment failed, show an error message
            return HttpResponse("Payment failed!")

    # Render the checkout template with the product details
    return render(request, 'checkout.html', {'product': product})
