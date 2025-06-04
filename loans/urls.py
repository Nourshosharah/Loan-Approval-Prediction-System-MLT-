from django.urls import path
from .views import loan_list

urlpatterns = [
    path('api/loans/', loan_list, name='loan_list'),
]
