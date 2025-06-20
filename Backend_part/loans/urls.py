from django.urls import path
from .views import home, loan_list, loan_detail,loan_summary,predict_loan



urlpatterns = [
    path('', home, name='home'), 
    path('api/loans/', loan_list, name='loan_list'),
    path('api/loans/<int:id>/', loan_detail, name='loan_detail'), 
    path('api/loans/summary/', loan_summary, name='loan_summary'),
    path('api/predict/', predict_loan, name='predict_loan'),



]

  






