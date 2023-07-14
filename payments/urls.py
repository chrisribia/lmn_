from django.urls import path
from .views import  home,getAccessToken,lipa_na_mpesa_online


urlpatterns = [
    path('', home, name='home'),  
    path('access/token', getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', lipa_na_mpesa_online, name='lipa_na_mpesa'),    
    ]