from django.urls import path
from .views import  home,getAccessToken,lipa_na_mpesa_online,register_urls,confirmation,validation,call_back


urlpatterns = [
    path('', home, name='home'),  
    path('access/token', getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', lipa_na_mpesa_online, name='lmn'),    

    # register, confirmation, validation and callback urls
    path('c2b/register', register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation', confirmation, name="confirmation"),
    path('c2b/validation', validation, name="validation"),
    path('c2b/callback', call_back, name="call_back"),
    ]
