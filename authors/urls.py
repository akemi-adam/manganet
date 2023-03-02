from django.urls import path
from . import views

urlpatterns = [
    
    #Generic routes
    
    path('dashboard', views.dashboard, name = 'dashboard'),

    # Author routes
    
    path('author', views.AuthorListView.as_view(), name = 'author.index'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name = 'author.show'),
    
    # Manga routes

    path('manga', views.MangaListView.as_view(), name = 'manga.index'),
    path('manga/<int:pk>', views.MangaDetailView.as_view(), name = 'manga.show'),
    path('manga/<int:id>/evaluation', views.store_evaluation, name = 'manga.evaluation.store'),
    path('manga/<int:id>/evaluation/destroy', views.destroy_evaluation, name = 'manga.evaluation.destroy'),
]