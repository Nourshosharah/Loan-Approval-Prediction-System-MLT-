# Create your views here.
from django.http import HttpResponse
from .models import Loan
import json

def loan_list(request):
    loans = Loan.objects.all().values()
    data = list(loans)
    json_data = json.dumps(data, indent=2)
    return HttpResponse(json_data, content_type="application/json")
