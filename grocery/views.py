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
        else:
            print(form.cleaned_data)
            product = Product.objects.filter(name=request.POST['name']).first()
            product.delete()
            product.quantity += form.cleaned_data['quantity']
            product.save()
            
    form = ProductForm()
    return render(request, 'add.html', {'formName': 'Add Product', 'form': form, 'submit_value': 'Add'})

@login_required(login_url='/login/')
def request_stock(request):
    if request.method == "POST":
        form = RequestsForm(request.POST)
        if form.is_valid():
            request_instance = Requests()
            request_instance.comment = form.cleaned_data['comment']
            request_instance.item_type = form.cleaned_data['item_type']
            request_instance.user = request.user
            request_instance.save()
    form = RequestsForm()
    return render(request, 'add.html', {'formName': 'Request', 'form': form, 'submit_value': 'REQUEST'})

@login_required(login_url='/login/')
def avaliable_stock(request):
    if (request.method == 'POST'):
        data = Product.objects.all().filter(quantity__gt = 0).order_by('quantity')
    else:
    
        data = Product.objects.all().filter(quantity__gt = 0)
    return render(request, 'stock.html', {'data': data})

@login_required(login_url='/login/')
def search_item(request):
    if request.method == 'POST':
        query = request.POST['search_string']
        similar_items_names = list(filter(lambda item: similarity_check(query, item), map(lambda x: x[0],Product.objects.values_list('name'))))
        similar_items = Product.objects.filter(name__in = similar_items_names)
        similar_types_names = list(filter(lambda item: similarity_check(query, item), map(lambda x: x[0],Type.objects.values_list('typename'))))
        similar_types = Type.objects.filter(typename__in = similar_types_names)
        return render(request, 'search.html', {'query':query, 'items': similar_items, 'types': similar_types})
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
def type_dashboard(request, value = None):
    
    if request.method == "POST":
        item_type = Type.objects.filter(typename = request.POST['typename']).first().id
        print(item_type)
        return redirect(f'/type/{item_type}')

    types = Type.objects.all()
    if value:
        type_obj = Type.objects.filter(id=value).first()

        products = Product.objects.filter(item_type = type_obj)

        qty = 0
        price = 0

        for item in products:
            qty+=item.quantity
            price += item.quantity*item.price
        
        

        return render(request, 'typedashboard.html', {'types':types, 'type': type_obj, 'items': products, 'total_items': qty, 'total_price': price})



    return render(request, 'typedashboard.html', {'types':types})


@login_required(login_url='/login/')
def item_desc(request, value):
    if request.method == 'POST':
        qty = request.POST['items']
        product = Product.objects.filter(id=request.POST['id']).first()
        product.quantity -= int(qty)
        product.save()
        if product.quantity == 0:
            return redirect('/avaliable/')

    item =  Product.objects.filter(id=value).first()



    return render(request, 'itemdash.html', {'item':item, 'total_amt': item.quantity*item.price})

@login_required(login_url='/login/')
def request_show(request):
    

    return render(request, 'requests.html', {'data': Requests.objects.all()})

@login_required(login_url='/login/')
def del_comment(request, value):
    comment = Requests.objects.filter(id=value).first()
    comment.delete()
    return redirect('/members/')

@login_required(login_url='/login/')
def sugest(request):
    item_sugession = Product.objects.filter(qty__lt = 6)
    # type_sugession = Product.objects.
    ...