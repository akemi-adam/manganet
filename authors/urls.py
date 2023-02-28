from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('author', views.index, name = 'author.index'),
    path('author/<int:id>', views.show, name = 'author.show'),
]