from django.contrib import admin
from .models import Author, Manga, Evaluation

admin.site.register(Author)
admin.site.register(Manga)
admin.site.register(Evaluation)