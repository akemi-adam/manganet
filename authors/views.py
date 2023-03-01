from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Author, Manga

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def index_author(request):
    return render(request, 'author/index.html', { 'authors': Author.objects.all().values() })


@login_required
def show_author(request, id):
    return render(request, 'author/show.html', { 'author': Author.objects.get(id = id) })

@login_required
def index_manga(request):
    return render(request, 'manga/index.html', { 'mangas': Manga.objects.all() })

@login_required
def show_manga(request, id):
    return render(request, 'manga/show.html', { 'manga': Manga.objects.get(id = id) })