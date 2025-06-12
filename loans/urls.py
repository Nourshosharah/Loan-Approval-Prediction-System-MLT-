from django.urls import path
from .views import home, loan_list



urlpatterns = [
    path('', home, name='home'), 
    path('api/loans/', loan_list, name='loan_list'),

]





