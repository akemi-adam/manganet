from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Author

@login_required
def dashboard(request):

    template = loader.get_template('dashboard.html')

    return HttpResponse(template.render())

@login_required
def index(request):
    
    authors = Author.objects.all().values()

    template = loader.get_template('index.html')
    
    context = {
        'authors': authors,
    }

    return HttpResponse(template.render(context, request))

@login_required
def show(request, id):

    author = Author.objects.get(id = id)

    template = loader.get_template('show.html')

    context = {
        'author': author,
    }

    return HttpResponse(template.render(context, request))