from django.shortcuts import render
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword 
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment
from django.http import HttpResponse, JsonResponse
 
# Create your views here.

def home(request):
    return render(request, 'home.html')


def getAccessToken(request):
    #consumer_key = 'ifeyg8caeO1616qZgFbiZ483PGuflCy1'
    access_token = MpesaAccessToken.validated_mpesa_access_token
    consumer_secret = 'gpoloXGtKliI8HqS'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)
def lipa_na_mpesa_online(request):
   # access_token = "MH9VMg0B8FXa61EbgMx1nW2GCs8N"
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254714577324,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254714577324,  # replace with your phone number to get stk push
        "CallBackURL":  "http://www.acaciatransportation.co/api/v1/c2b/confirmation",
        "AccountReference": "Christopher ribia",
        "TransactionDesc": "Django Shop stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse(response)
@csrf_exempt
def register_urls(request):
    #access_token = "MH9VMg0B8FXa61EbgMx1nW2GCs8N"
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "http://www.acaciatransportation.co/api/v1/c2b/confirmation",
               "ValidationURL": "http://www.acaciatransportation.co//api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

@csrf_exempt
def call_back(request):
    pass
@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
 
    payment = MpesaPayment(
    first_name=mpesa_payment['FirstName'],
    last_name=mpesa_payment['LastName'],
    middle_name=mpesa_payment['MiddleName'],
    description=mpesa_payment['TransID'],
    phone_number=mpesa_payment['MSISDN'],
    amount=mpesa_payment['TransAmount'],
    reference=mpesa_payment['BillRefNumber'],
    organization_balance=mpesa_payment['OrgAccountBalance'],
    type=mpesa_payment['TransactionType'],
    )
    payment.save()
 
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse(json.dumps({"ResultCode": 0, "ResultDesc": "Callback received."}), content_type="application/json")
 
 
def checkout(request):
    # Retrieve the selected product 

    if request.method == 'POST':
        # Base64 encode the consumer_key and consumer_secret
        consumer_key = ' ifeyg8caeO1616qZgFbiZ483PGuflCy1'
        consumer_secret = 'gpoloXGtKliI8HqS'
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
            'BusinessShortCode': LipanaMpesaPpassword.Business_short_code,
            'Password': base64.b64encode(f'{YOUR_SHORTCODE_PASSKEY}{timestamp}'.encode()).decode(),
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': 1,
            'PartyA': 254714577324,
            'PartyB': LipanaMpesaPpassword.Business_short_code,
            'PhoneNumber': 254714577324,
            'CallBackURL': 'https://example.com/callback',
            'AccountReference': 'YOUR_REFERENCE',
            'TransactionDesc':'Tral'
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
    return render(request, 'home.html', {'product': product})
