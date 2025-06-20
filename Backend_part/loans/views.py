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


model_path = os.path.join(os.path.dirname(__file__), 'DecisionTree_mode.pkl')
model = joblib.load(model_path)

@api_view(['POST'])
def predict_loan(request):
    try:
        data = request.data

        total_income = float(data['applicant_income']) + float(data['coapplicant_income'])
        loan_amount = float(data['loan_amount'])
        loan_term_months = float(data['loan_amount_term'])
        monthly_payment = loan_amount / loan_term_months if loan_term_months else 0

        gender_male = 1 if data['gender'].lower() == 'male' else 0
        married_yes = 1 if data['married'].lower() == 'yes' else 0

        dependents_1 = 1 if data['dependents'] == '1' else 0
        dependents_2 = 1 if data['dependents'] == '2' else 0
        dependents_3plus = 1 if data['dependents'] in ['3', '3+'] else 0

        education_not_grad = 1 if data['education'].lower() == 'not graduate' else 0
        self_employed_yes = 1 if data['self_employed'].lower() == 'yes' else 0

        property_area_semiurban = 1 if data['property_area'].lower() == 'semiurban' else 0
        property_area_urban = 1 if data['property_area'].lower() == 'urban' else 0
  

        credit_history = int(data['credit_history'])  


        features = np.array([[
            credit_history,
            gender_male,
            married_yes,
            dependents_1,
            dependents_2,
            dependents_3plus,
            education_not_grad,
            self_employed_yes,
            property_area_semiurban,
            property_area_urban,
            total_income,
            monthly_payment
        ]])

        prediction = model.predict(features)[0]
        result = "Approved" if prediction == "Y" else "Rejected"
        return Response({"prediction": result})

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
