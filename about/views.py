from django.shortcuts import render

# Create your views here.
def about_page(request):
    data = {'dev': 'Rohit Singh', 'github':'https://github.com/RohitSingh-04', 'linkedin':'https://www.linkedin.com/in/rohit-singh-a59407274/'}
    return render(request, 'about.html', {'data': data})