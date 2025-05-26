import pandas as pd
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loan_project.settings")
django.setup()

from loans.models import Loans
df = pd.read_csv("loan_data.csv")

for index, row in df.iterrows():
    Loans.objects.create(
        loan_id=row['Loan_ID'],
        gender=row['Gender'],
        married=row['Married'],
        dependents=row['Dependents'],
        education=row['Education'],
        self_employed=row['Self_Employed'],
        applicant_income=row['ApplicantIncome'],
        coapplicant_income=row['CoapplicantIncome'],
        loan_amount=row['LoanAmount'],
        loan_amount_term=row['Loan_Amount_Term'],
        credit_history=row['Credit_History'],
        property_area=row['Property_Area'],
        loan_status=row['Loan_Status'],
    )

print("Data loaded successfully.")
