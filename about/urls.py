from django.urls import path
from . import views

urlpatterns = [

    path('about/', view = views.about_page)

]