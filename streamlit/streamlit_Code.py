
import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
import sklearn
print(np.__version__)
print(sklearn.__version__)
def preprocess_cols(df,featuers,caps):
    df=df.copy()
    object_cols=df.select_dtypes(include="object").columns.tolist()
  

    df["ApplicantIncome_log"]=np.log(df["ApplicantIncome"])
    df["LoanAmount_log"]=np.log(df["LoanAmount"])
    df["CoapplicantIncome_log"]=np.log1p(df["CoapplicantIncome"])
    for col in df[["ApplicantIncome_log","LoanAmount_log","CoapplicantIncome_log"]]:
        if caps is not None:
            lower, upper =caps[col]
        else :
            lower, upper =-np.inf, np.inf
        df[col+"_updated"]=np.where (df[col]< lower, lower,np.where(df[col]>upper, upper, df[col]))
    df_final=pd.get_dummies(df, columns=object_cols)
    print(df_final.columns)
    df_final["Total_income"]=df_final["ApplicantIncome_log_updated"]+df_final["CoapplicantIncome_log_updated"]
    df_final["month_payment"]=df_final["LoanAmount_log_updated"]/df_final["Loan_Amount_Term"]
    df_final.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_final.fillna(0, inplace=True)
    df_final = df_final.reindex(columns=featuers, fill_value=False)

    return df_final 


DATA_PATH = "loan_prediction.csv"
if os.path.exists(DATA_PATH):
    loans_df = pd.read_csv(DATA_PATH)
else:
    loans_df = pd.DataFrame(columns=['Loan_ID', 'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area', 'Loan_Status']
                            )

model = joblib.load("DecisionTree_mode.pkl")
import pickle

# with open(r"C:\Users\Nour Shosharah\DecisionTree_mode.pkl", 'rb') as f:
#     model = pickle.load(f)

st.sidebar.title("Loan Streamlit App")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📋 Loan List", "📌 Loan Detail", "📊 Loan Summary", "🔮 Predict Loan Status"]
)

if page == "🏠 Home":
    st.title("Welcome to the Loan Streamlit App")
    st.write("Use the sidebar to navigate pages.")

elif page == "📋 Loan List":
    st.title("All Loans")
    st.dataframe(loans_df)

    st.subheader("Add New Loan")
    with st.form("add_loan_form"):
        new_loan = {
            'loan_id': st.text_input("Loan ID"),
            'gender': st.selectbox("Gender", ["Male", "Female"]),
            'married': st.selectbox("Married", ["Yes", "No"]),
            'dependents': st.selectbox("Dependents", ["0", "1", "2", "3+"]),
            'education': st.selectbox("Education", ["Graduate", "Not Graduate"]),
            'self_employed': st.selectbox("Self Employed", ["Yes", "No"]),
            'applicant_income': st.number_input("Applicant Income", min_value=0),
            'coapplicant_income': st.number_input("Coapplicant Income", min_value=0.0),
            'loan_amount': st.number_input("Loan Amount", min_value=0.0),
            'loan_amount_term': st.number_input("Loan Amount Term", min_value=0.0),
            'credit_history': st.selectbox("Credit History", [1.0, 0.0]),
            'property_area': st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"]),

        }

        submitted = st.form_submit_button("Add Loan")
        if submitted:
            loans_df.loc[len(loans_df)] = new_loan
            loans_df.to_csv(DATA_PATH, index=False)
            st.success("Loan added successfully!")

elif page == "📌 Loan Detail":
    st.title("Loan Detail")
    loan_id = st.selectbox("Loan_ID", loans_df.Loan_ID.unique())
    print(loan_id)
    if loan_id in loans_df.Loan_ID.unique():
        loan = loans_df[loans_df['Loan_ID'] == loan_id]
        print(loan)
        st.write(loan)

        st.subheader("Edit Loan")
        with st.form("edit_loan_form"):
            current_status = loan['Loan_Status'].iloc[0]  
            updated_status = st.selectbox(
                "Loan_Status",
                ["Y", "N"],
                index=["Y", "N"].index(current_status)
            )
            if st.form_submit_button("Update"):
                loans_df.loc[loans_df['Loan_ID'] == loan_id, 'Loan_Status'] = updated_status
                loans_df.to_csv(DATA_PATH, index=False)
                st.success("Loan updated successfully!")

        if st.button("Delete Loan"):
            loans_df.drop(loans_df[loans_df['Loan_ID'] == loan_id].index, inplace=True)
            loans_df.to_csv(DATA_PATH, index=False)
            st.success("Loan deleted successfully!")
    else:
        st.warning("Loan ID not found.")


elif page == "📊 Loan Summary":
    st.title("Loan Summary")
    approved = loans_df[loans_df['Loan_Status'] == 'Y'].shape[0]
    rejected = loans_df[loans_df['Loan_Status'] == 'N'].shape[0]
    total = loans_df.shape[0]
    avg_income = loans_df['ApplicantIncome'].mean() if total > 0 else 0
    st.subheader("Dataset Statistic ")
    st.metric("Total Loans", total)
    st.metric("Approved", approved)
    st.metric("Rejected", rejected)
    st.metric("Avg Applicant Income", f"{avg_income:.2f}")
    
   
    st.subheader("Dataset Overview")
    st.write(loans_df.describe())
    st.write(loans_df.describe(include="object"))


    st.subheader("Missing Values Before")
    st.write(loans_df.isnull().sum() / loans_df.shape[0])

  
    for col in ['Gender', 'Married', 'Dependents', 'Self_Employed']:
        loans_df[col].fillna(loans_df[col].mode()[0], inplace=True)

 
    loans_df["LoanAmount"].fillna(loans_df["LoanAmount"].median(), inplace=True)
    loans_df["Loan_Amount_Term"].fillna(loans_df["Loan_Amount_Term"].mode()[0], inplace=True)
    loans_df["Credit_History"].fillna(loans_df["Credit_History"].mode()[0], inplace=True)

   
    st.subheader("Missing Values After")
    st.write(loans_df.isnull().sum() / loans_df.shape[0])

  
    st.subheader("Categorical Distributions")
    object_cols = loans_df.select_dtypes(include="object").drop(columns="Loan_ID")
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    for col in object_cols.columns:
        value_counts = object_cols[col].value_counts(normalize=True) * 100
        labels = value_counts.index
        values = value_counts.values
        cmap = cm.get_cmap("Pastel1", len(labels))
        colors = [cmap(i) for i in range(len(labels))]

        fig, ax = plt.subplots()
        ax.bar(labels, values, color=colors)
        ax.set_title(f"Values for {col}")
        ax.set_ylabel("Percentage")
        ax.set_xlabel(col)
        st.pyplot(fig)

   
    st.subheader("Numerical Distributions (Histograms)")
    numerical_features = loans_df.select_dtypes(exclude="object").columns

    for col in numerical_features:
        fig, ax = plt.subplots()
        loans_df[col].hist(bins=30, ax=ax)
        ax.set_title(f"Histogram for {col}")
        st.pyplot(fig)

    import seaborn as sns
    st.subheader("Boxplots for Numerical Features")
    for col in numerical_features:
        fig, ax = plt.subplots()
        sns.boxplot(x=loans_df[col], ax=ax)
        ax.set_title(f"Boxplot for {col}")
        st.pyplot(fig)

 
    st.subheader("Log Transform & Outlier Capping")
    loans_df["ApplicantIncome_log"] = np.log(loans_df["ApplicantIncome"])
    loans_df["LoanAmount_log"] = np.log(loans_df["LoanAmount"])
    loans_df["CoapplicantIncome_log"] = np.log1p(loans_df["CoapplicantIncome"])

    for col in ["ApplicantIncome_log", "LoanAmount_log", "CoapplicantIncome_log"]:
        Q1 = loans_df[col].quantile(0.25)
        Q3 = loans_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        loans_df[col + "_updated"] = np.clip(loans_df[col], lower, upper)

   
    for col in ["ApplicantIncome_log", "LoanAmount_log", "CoapplicantIncome_log"]:
        fig, ax = plt.subplots()
        sns.boxplot(x=loans_df[col + "_updated"], ax=ax)
        ax.set_title(f"Boxplot for {col} (Capped)")
        st.pyplot(fig)
    st.subheader("Correlation with Loan_Status")
    st.image("correlation_heatmap.png", caption="Feature Correlation", use_column_width=True)


    st.write("✅ EDA Completed")


elif page == "🔮 Predict Loan Status":
    st.title("Predict Loan Approval")

 
    with st.form("predict_form"):
        gender = st.selectbox("Gender", ["Male", "Female"])
        married = st.selectbox("Married", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])
        self_employed = st.selectbox("Self Employed", ["Yes", "No"])
        applicant_income = st.number_input("Applicant Income", min_value=0)
        coapplicant_income = st.number_input("Coapplicant Income", min_value=0.0)
        loan_amount = st.number_input("Loan Amount", min_value=0.0)
        loan_amount_term = st.number_input("Loan Amount Term", min_value=0.0)
        credit_history = st.selectbox("Credit History", [1.0, 0.0])
        property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

        submit = st.form_submit_button("Predict")

    if submit:
     
        test_data = {
            "Gender": gender,
            "Married": married,
            "Dependents": dependents,
            "Education": education,
            "Self_Employed": self_employed,
            "ApplicantIncome": applicant_income,
            "CoapplicantIncome": coapplicant_income,
            "LoanAmount": loan_amount,
            "Loan_Amount_Term": loan_amount_term,
            "Credit_History": credit_history,
            "Property_Area": property_area
        }
        test_df = pd.DataFrame([test_data])

        
        features = [
            'Credit_History',
            'Gender_Male',
            'Married_Yes',
            'Dependents_1',
            'Dependents_2',
            'Dependents_3+',
            'Education_Not Graduate',
            'Self_Employed_Yes',
            'Property_Area_Semiurban',
            'Property_Area_Urban',
            'Total_income',
            'month_payment'
        ]

        caps = {
            "ApplicantIncome_log": (6.914567376450192, 9.714858994637867),
            "LoanAmount_log": (3.8625058531812333, 5.849577627901635),
            "CoapplicantIncome_log": (-11.609845226339234, 19.349742043898722)
        }

        df_test_model=preprocess_cols(test_df,features,caps)
        print(df_test_model.columns)
        y_pred=model.predict(df_test_model)
        print(y_pred)
        if y_pred in [1, True, 'Y']:
            result_text = "✅ Approved"
        else:
            result_text = "❌ Denied"

       
        st.info(f"**Predicted Result is :** {result_text}")

