from django.urls import path
from . import views


urlpatterns = [
    path('', view=views.home),
    path('register/', view=views.user_register),
    path('login/', view=views.login_usr),
    path('logout/', view=views.logout_usr),
    path('addType/', view=views.new_type),
    path('addProduct/', view=views.product_register),
    path('Request/', view=views.request_stock),
    path('avaliable/', view=views.avaliable_stock),
    path('search/', view= views.search_item),
    path('type/', view=views.type_dashboard)
]