from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import Author, Manga, Evaluation

@login_required
def dashboard(request) -> HttpResponse:
    return render(request, 'dashboard.html')

# Author controllers

@method_decorator(login_required, name = 'dispatch')
class AuthorListView(ListView):
    
    model: Author = Author
    
    template_name: str = 'author/index.html'
    
    context_object_name: str = 'authors'

@method_decorator(login_required, name = 'dispatch')
class AuthorDetailView(DetailView):
    
    model: Author = Author
    
    template_name: str = 'author/show.html'
    
    context_object_name: str = 'author'

# Manga controllers

@method_decorator(login_required, name = 'dispatch')
class MangaListView(ListView):

    model: Manga = Manga
    
    template_name: str = 'manga/index.html'
    
    context_object_name: str = 'mangas'

@method_decorator(login_required, name = 'dispatch')
class MangaDetailView(DetailView):

    model: Manga = Manga

    template_name: str = 'manga/show.html'

    context_object_name: str = 'manga'

    def get_context_data(self, **kwargs: Any):

        context = super().get_context_data(**kwargs)
        
        context['is_rated'] = self.get_object().users.contains(self.request.user)
        
        return context
    
@login_required
def store_evaluation(request: HttpRequest, id: int) -> HttpResponseRedirect | HttpResponsePermanentRedirect:

    manga: Manga = Manga.objects.get(id = id)

    user = request.user

    rating = request.POST.get('rating')

    evaluationExists: QuerySet = Evaluation.objects.filter(manga_id = manga.id, user_id = user.id)

    if evaluationExists.exists():

        evaluation: Evaluation = evaluationExists.get()

        evaluation.rating = rating

        evaluation.save()

    else:
        manga.users.add(user, through_defaults = {'rating': rating})

    return redirect('profile', id = user.id)

@login_required
def destroy_evaluation(request: HttpRequest, id: int) -> HttpResponseRedirect | HttpResponsePermanentRedirect:

    if request.method != 'POST':
        return redirect('dashboard')

    manga: Manga = Manga.objects.get(id = id)

    user = request.user

    evaluation: Evaluation = Evaluation.objects.filter(manga_id = manga.id, user_id = user.id).get()

    evaluation.delete()

    return redirect('profile', id = user.id)