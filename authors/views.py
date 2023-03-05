from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.db.models.query import QuerySet

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.db import connection

from .models import Author, Manga, Evaluation

# Aux functions

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def top_rated_mangas():

    with connection.cursor() as cursor:

        cursor.execute('SELECT * FROM fn_topRatedMangas()')

        top_rated_mangas = dictfetchall(cursor)

    return top_rated_mangas

# Dashboard Controller

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """ Returns dashboard page if user is logged in, where it shows the 3 most recent manga and the 5 best rated manga"""

    latest_mangas = Manga.objects.order_by('-id')[:3]

    return render(request, 'dashboard.html', {
        'latest_mangas': latest_mangas,
        'top_rated_mangas': top_rated_mangas()
    })

# Author controllers

@method_decorator(login_required, name = 'dispatch')
class AuthorListView(ListView):
    """ Shows the list of authors if the user is logged in """
    
    model: Author = Author
    
    template_name: str = 'author/index.html'
    
    context_object_name: str = 'authors'

@method_decorator(login_required, name = 'dispatch')
class AuthorDetailView(DetailView):
    """ Shows the detail of a specif author if the user is logged in """

    model: Author = Author
    
    template_name: str = 'author/show.html'
    
    context_object_name: str = 'author'

# Manga controllers

@method_decorator(login_required, name = 'dispatch')
class MangaListView(ListView):
    """ Shows the list of mangas if the user is logged in """

    model: Manga = Manga
    
    template_name: str = 'manga/index.html'
    
    context_object_name: str = 'mangas'

    paginate_by = 5

@method_decorator(login_required, name = 'dispatch')
class MangaDetailView(DetailView):
    """ Shows the detail of a specif manga if the user is logged in """

    model: Manga = Manga

    template_name: str = 'manga/show.html'

    context_object_name: str = 'manga'

    def get_context_data(self, **kwargs: Any):

        context = super().get_context_data(**kwargs)
        
        context['is_rated'] = self.get_object().users.contains(self.request.user)

        context['comments'] = self.get_object().evaluation_set.all()
        
        return context
    
@login_required
def store_evaluation(request: HttpRequest, id: int) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    """ Saves a user's rating of a particular manga. If the rating has already been done, overwrites the previous one with the new one. Redirects to the user's profile """

    manga: Manga = Manga.objects.get(id = id)

    user = request.user

    rating = request.POST.get('rating')

    comment = request.POST.get('comment')

    evaluationExists: QuerySet = Evaluation.objects.filter(manga_id = manga.id, user_id = user.id)

    if evaluationExists.exists():

        evaluation: Evaluation = evaluationExists.get()

        if rating != evaluation.rating:
            evaluation.rating = rating

        if comment != None and comment != '':
           evaluation.comment = comment

        evaluation.save()

    else:
        manga.users.add(user, through_defaults = { 'rating': rating, 'comment': comment })

    return redirect('profile', id = user.id)

@login_required
def destroy_evaluation(request: HttpRequest, id: int) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    """ Remove a rating """

    if request.method != 'POST':
        return redirect('dashboard')

    manga: Manga = Manga.objects.get(id = id)

    user = request.user

    evaluation: Evaluation = Evaluation.objects.filter(manga_id = manga.id, user_id = user.id).get()

    evaluation.delete()

    return redirect('profile', id = user.id)