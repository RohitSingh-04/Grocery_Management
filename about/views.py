from django.shortcuts import render

# Create your views here.
def about_page(request):
    data = {'dev': 'Rohit Singh', 'github':'', 'linkedin':''}
    return render(request, 'about.html', {'data': data})