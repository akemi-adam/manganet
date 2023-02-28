from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Author, Manga

@login_required
def dashboard(request):

    template = loader.get_template('dashboard.html')

    return HttpResponse(template.render())

@login_required
def index_author(request):
    
    authors = Author.objects.all().values()

    template = loader.get_template('author/index.html')
    
    context = {
        'authors': authors,
    }

    return HttpResponse(template.render(context, request))

@login_required
def show_author(request, id):

    author = Author.objects.get(id = id)

    template = loader.get_template('author/show.html')

    context = {
        'author': author,
    }

    return HttpResponse(template.render(context, request))

@login_required
def index_manga(request):

    mangas = Manga.objects.all()

    return render(request, 'manga/index.html', {'mangas': mangas})

@login_required
def show_manga(request, id):

    manga = Manga.objects.get(id = id)

    return render(request, 'manga/show.html', {'manga': manga})