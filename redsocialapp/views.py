from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def ingreso(request):
    if request.method == "GET":
        return render(request,'ingreso.html')
    
def registro(request):
    if request.method == "GET":
        return render(request,'registro.html')