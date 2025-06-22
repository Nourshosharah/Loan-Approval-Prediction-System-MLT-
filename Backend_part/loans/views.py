# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from .serializers import LoanSerializer
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Avg
import joblib
import numpy as np
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import json



def home(request):
    return HttpResponse("<h2>Welcome to the Loan API</h2>")

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



def preprocess_cols(df, features, caps):
    df = df.copy()
    object_cols = df.select_dtypes(include="object").columns.tolist()
    if "Loan_ID" in object_cols:
        object_cols.remove("Loan_ID")
    if "Loan_Status" in object_cols:
        object_cols.remove("Loan_Status")

    df["ApplicantIncome_log"] = np.log(df["ApplicantIncome"])
    df["LoanAmount_log"] = np.log(df["LoanAmount"])
    df["CoapplicantIncome_log"] = np.log1p(df["CoapplicantIncome"])

    for col in ["ApplicantIncome_log", "LoanAmount_log", "CoapplicantIncome_log"]:
        if caps is not None:
            lower, upper = caps[col]
        else:
            lower, upper = -np.inf, np.inf
        df[col + "_updated"] = np.where(
            df[col] < lower, lower, np.where(df[col] > upper, upper, df[col])
        )

    df_final = pd.get_dummies(df, columns=object_cols)
    df_final["Total_income"] = df_final["ApplicantIncome_log_updated"] + df_final["CoapplicantIncome_log_updated"]
    df_final["month_payment"] = df_final["LoanAmount_log_updated"] / df_final["Loan_Amount_Term"]
    df_final = df_final.reindex(columns=features, fill_value=0)

    return df_final


model_path = r'C:\Users\omar_oz\Desktop\MCS\F24\HW_F24_MLT\MLT_Project\Backend_part\loans\DecisionTree_mode.pkl'
with open(model_path, 'rb') as f:
    model = joblib.load(f)
    features = [
    "Credit_History",
    "Gender_Male",
    "Married_Yes",
    "Dependents_1",
    "Dependents_2",
    "Dependents_3+",
    "Education_Not Graduate",
    "Self_Employed_Yes",
    "Property_Area_Semiurban",
    "Property_Area_Urban",
    "Total_income",
    "month_payment",
]

caps = {
    "ApplicantIncome_log": (6.914567376450192, 9.714858994637867),
    "LoanAmount_log": (3.8625058531812333, 5.849577627901635),
    "CoapplicantIncome_log": (-11.609845226339234, 19.349742043898722),
}

@csrf_exempt
def predict_loan_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            df_input = pd.DataFrame([data])
            df_processed = preprocess_cols(df_input, features, caps)

            prediction = model.predict(df_processed)[0]
            proba = model.predict_proba(df_processed)[0].tolist()

            result = {
                "prediction": bool(prediction),
                "probability": {"Rejected": proba[0], "Accepted": proba[1]},
            }

            return JsonResponse(result)

        except Exception as error:
            return JsonResponse({"error": str(error)}, status=400)

    else:
        return JsonResponse({"error": "Only POST requests ."}, status=405)




