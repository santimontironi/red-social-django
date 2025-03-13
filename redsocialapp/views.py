from django.shortcuts import render

# Create your views here.
def ingreso(request):
    if request.method == "GET":
        return render(request,'ingreso.html')
    