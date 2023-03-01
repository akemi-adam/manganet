from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('author', views.index_author, name = 'author.index'),
    path('author/<int:id>', views.show_author, name = 'author.show'),
    path('manga', views.index_manga, name = 'manga.index'),
    path('manga/<int:id>', views.show_manga, name = 'manga.show'),
    path('manga/<int:id>/evaluation', views.evaluation, name = 'manga.evaluation'),
]