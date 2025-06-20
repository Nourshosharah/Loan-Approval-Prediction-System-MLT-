from django.urls import path
from .views import home, loan_list, loan_detail,loan_summary,predict_loan




urlpatterns = [
    path('', home, name='home'), 
    path('loans/', loan_list, name='loan_list'),
    path('loans/<int:id>/', loan_detail, name='loan_detail'), 
    path('loans/summary/', loan_summary, name='loan_summary'),
    path('predict/', predict_loan, name='predict_loan'),
]



  






