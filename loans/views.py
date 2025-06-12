# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from .serializers import LoanSerializer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Avg
import joblib
import numpy as np
import os


def home(request):
    return HttpResponse("<h2>Welcome to the Loan API </h2><p>Go to <a href='/api/loans/'>/api/loans/</a> to see all loans.</p>")

@api_view(['GET', 'POST'])
def loan_list(request):
    if request.method == 'GET':
        loans = Loan.objects.all()  
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT', 'DELETE'])
def loan_detail(request, id):
    loan = get_object_or_404(Loan, id=id)

    if request.method == 'GET':
        serializer = LoanSerializer(loan)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = LoanSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def loan_summary(request):
    approved = Loan.objects.filter(loan_status='Y').count()
    rejected = Loan.objects.filter(loan_status='N').count()
    total = Loan.objects.count()
    avg_income = Loan.objects.aggregate(Avg('applicant_income'))['applicant_income__avg']

    return Response({
        "total_loans": total,
        "approved": approved,
        "rejected": rejected,
        "avg_applicant_income": avg_income,
    })


model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = joblib.load(model_path)

@api_view(['POST'])
def predict_loan(request):
    try:
        data = request.data
    
        features = np.array([[
            data['gender'],
            data['married'],
            data['dependents'],
            data['education'],
            data['self_employed'],
            data['applicant_income'],
            data['coapplicant_income'],
            data['loan_amount'],
            data['loan_amount_term'],
            data['credit_history'],
            data['property_area']
        ]])

        prediction = model.predict(features)[0]
        result = "Approved" if prediction == "Y" else "Rejected"
        return Response({"prediction": result})
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

