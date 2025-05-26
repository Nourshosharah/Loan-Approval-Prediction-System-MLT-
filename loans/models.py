from django.db import models

class Loans(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARRIED_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    EDUCATION_CHOICES = [('Graduate', 'Graduate'), ('Not Graduate', 'Not Graduate')]
    SELF_EMPLOYED_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    PROPERTY_CHOICES = [('Urban', 'Urban'), ('Rural', 'Rural'), ('Semiurban', 'Semiurban')]
    STATUS_CHOICES = [('Y', 'Approved'), ('N', 'Rejected')]

    loan_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    married = models.CharField(max_length=5, choices=MARRIED_CHOICES, null=True, blank=True)
    dependents = models.CharField(max_length=5, null=True, blank=True)
    education = models.CharField(max_length=15, choices=EDUCATION_CHOICES)
    self_employed = models.CharField(max_length=5, choices=SELF_EMPLOYED_CHOICES, null=True, blank=True)
    applicant_income = models.FloatField()
    coapplicant_income = models.FloatField()
    loan_amount = models.FloatField(null=True, blank=True)
    loan_amount_term = models.FloatField(null=True, blank=True)
    credit_history = models.FloatField(null=True, blank=True)
    property_area = models.CharField(max_length=20, choices=PROPERTY_CHOICES)
    loan_status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.loan_id} - {self.loan_status}"
