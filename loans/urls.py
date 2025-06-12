from django.urls import path
from .views import home, loan_list, loan_detail



urlpatterns = [
    path('', home, name='home'), 
    path('api/loans/', loan_list, name='loan_list'),
    path('api/loans/<int:id>/', loan_detail, name='loan_detail'), 
  
]





