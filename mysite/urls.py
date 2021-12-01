from mysite.models import farmer
from .views import homepage,agentpage,transactionpage,farmerunderagent,farmerpage,downloadpdf,user_login,user_logout
from django.urls import path

urlpatterns = [
    path('',homepage,name="homepage"),
    path('agent',agentpage,name="agentpage"),
    path('transaction',transactionpage,name="transactionpage"),
    path('farmer',farmerpage,name='farmerpage'),
    path('farmerunderagent',farmerunderagent,name="farmerunderagent"),
    path('downloadpdf',downloadpdf,name='downloadpdf'),
    path('login',user_login,name='login'),
    path('logout',user_logout,name='logout'),

]