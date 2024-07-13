from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Sum, F
from .forms import *

def login_usr(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Invalid username or password')
                return render(request, 'add.html', {'formName':'Login', 'form': form, 'after_form': '<p>Do not have an Account? <a href="/register/">Register</a> First!</p>', 'submit_value':'Login'})
    form = AuthenticationForm(request=request)
    return render(request, 'add.html', {'formName':'Login', 'form': form, 'after_form': '<p>Do not have an Account? <a href="/register/">Register</a> First!</p>', 'submit_value':'Login'})

def logout_usr(request):
    logout(request)
    return redirect('/login')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    form = UserCreationForm()
    return render(request, 'add.html', {'formName': 'Registration', 'form': form, 'after_form': '<p>Already have an Account? <a href="/login/">Login</a> Insteed!</p>', 'submit_value': 'Register'})

@login_required(login_url='/login/')
def home(request):
    total_items = Product.objects.aggregate(total_items = Sum('quantity'))['total_items']
    total_price = Product.objects.annotate(total_val= F('price') * F('quantity')).aggregate(total = Sum('total_val'))['total']

    
    return render(request, 'index.html', {'total_stock': total_items, 'total_price': total_price})

@login_required(login_url='/login')
def new_type(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            form = TypeForm()
            return render(request, 'add.html', {'formName': 'Add Type', 'form': form, 'submit_value': 'Add', 'after_form': '''<div class="alert alert-success alert-dismissible fade show" role="alert">
  <strong>Success!</strong> added the new type.
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>'''})

    form = TypeForm()
    return render(request, 'add.html', {'formName': 'Add Type', 'form': form, 'submit_value': 'Add'})

@login_required(login_url='/login/')
def product_register(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():

            product = form.save(commit=False)
            product.save()
            form.save_m2m()
    
    form = ProductForm()
    return render(request, 'add.html', {'formName': 'Add Product', 'form': form, 'submit_value': 'Add'})

@login_required(login_url='/login/')
def request_stock(request):
    if request.method == "POST":
        form = RequestsForm(request.POST)
        if form.is_valid():
            form.save()
    
    form = RequestsForm()
    return render(request, 'add.html', {'formName': 'Request', 'form': form, 'submit_value': 'REQUEST'})

@login_required(login_url='/login/')
def avaliable_stock(request):
    data = Product.objects.all()
    return render(request, 'stock.html', {'data': data})

@login_required(login_url='/login/')
def search_item(request):
    if request.method == 'POST':
        query = request.POST['search_string']
        similar_items_names = list(filter(lambda item: similarity_check(query, item), map(lambda x: x[0],Product.objects.values_list('name'))))
        similar_items = Product.objects.filter(name__in = similar_items_names)
        similar_types_names = list(filter(lambda item: similarity_check(query, item), map(lambda x: x[0],Type.objects.values_list('typename'))))
        similar_types = Type.objects.filter(typename__in = similar_types_names)
        return render(request, 'search.html', {'items': similar_items, 'types': similar_types})
    return render(request, 'search.html')

def similarity_check(search: str, result: str, threshold:float = 0.5) -> bool:
    
    """
    Check similarity between two strings based on the proportion of matching characters.

    Parameters:
    search (str): The search string.
    result (str): The result string to compare against.
    threshold (float): The similarity threshold ranging from 0 to 1, where 1 is highly similar and 0 is least similar.

    Returns:
    bool: True if the similarity ratio is greater than or equal to the threshold, False otherwise.
    """
    if not search:
        return False
    
    search_set = set(search.lower())
    result_set = set(result.lower())

    matched = sum(1 for char in search_set if char in result_set)
    
    return matched/len(result_set) >= threshold 

@login_required(login_url='/login/')
def type_dashboard(request):
    form = TypeDashForm()
    return render(request, 'typedashboard.html', {'form':form})