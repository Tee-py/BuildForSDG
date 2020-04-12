from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def xml(request):
    return render(request, "xml.html")

def json(request):
    return render(request, "json.html")

def logs(request):
    return render(request, "logs.html")
