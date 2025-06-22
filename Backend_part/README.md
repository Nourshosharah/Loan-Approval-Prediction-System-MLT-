# Loan Approval API Backend
Django , Django REST Framework , Scikit-learn

# Endpoints

| Path                      | Methods                | Description                                             |
|---------------------------|------------------------|----------------------------------|
| `/`                       | GET                    | Welcome page with API links       |
| `/api/loans/`             | GET, POST              | List all loans, create new loan   |
| `/api/loans/<id>/`        | GET, PUT, DELETE       | Retrieve, update or delete a loan |
| `/api/loans/summary/`     | GET                    | Summary statistics (approved, rejected, average income) |
| `/api/predict/`           | POST                   | Predict approval or rejection for a new loan request    |

## API Details
## 1. Loan List and Create
- **GET** `/api/loans/`  
  Retrieves all stored loan requests.

- **POST** `/api/loans/`  
  Adds a new loan request.  
  **Request Body (JSON):**  
  ```json
  {
    "loan_id": "LN123",
    "gender": "Male",
    "married": "Yes",
    "dependents": "0",
    "education": "Graduate",
    "self_employed": "No",
    "applicant_income": 5000,
    "coapplicant_income": 0.0,
    "loan_amount": 150.0,
    "loan_amount_term": 360.0,
    "credit_history": 1.0,
    "property_area": "Urban",
    "loan_status": "Y"
  }
 ## 2. Loan Detail, Update, and Delete
** GET ** /api/loans/<id>/ 
Retrieve a loan request by ID.
 ** PUT  ** /api/loans/<id>/
Update a loan request by ID.
Request Body: Same as above for creating loan.
 ** DELETE  ** /api/loans/<id>/
Delete a loan request by ID.
## 3. Loan Summary
** GET  ** /api/loans/summary/
Returns statistics about loans:
{
  "total_loans": 100,
  "approved": 70,
  "rejected": 30,
  "avg_applicant_income": 4500.75
}
## 4. Predict Loan Approval
**POST **  /api/predict/
Submit loan features to get approval prediction.
Request Body Example:
json
Copy
Edit
{
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

}
Response Example:
{
  "prediction": true,
  "probability": {
    "Rejected": 0.2,
    "Accepted": 0.8
  }
}

CORS
All origins are allowed by default (CORS_ALLOW_ALL_ORIGINS = True), enabling frontend communication easily.



