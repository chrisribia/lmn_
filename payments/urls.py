from django.urls import path
from .views import  home,getAccessToken,lipa_na_mpesa_online,register_urls,confirmation,validation,call_back,checkout


urlpatterns = [
    path('name/', home, name='name'),  
    path('token', getAccessToken, name='token'),
    path('lmn', checkout, name='lmn'),    

    # register, confirmation, validation and callback urls
    path('register', register_urls, name="register"),
    path('c2b/confirmation', confirmation, name="confirmation"),
    path('c2b/validation', validation, name="validation"),
    path('c2b/callback', call_back, name="call_back"),
    ]
