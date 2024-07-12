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

    
    return HttpResponse("home")

@login_required(login_url='/login')
def new_type(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()

    form = TypeForm()
    return render(request, 'add.html', {'formName': 'Add Product Type', 'form': form, 'submit_value': 'Add'})

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
