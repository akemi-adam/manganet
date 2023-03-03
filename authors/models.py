from django.db import models
from django.contrib.auth import get_user_model

class Author(models.Model):

    name = models.CharField(max_length=125, verbose_name = 'Nome')
    
    age = models.IntegerField(verbose_name = 'Idade')

    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE, verbose_name = 'Usuário')

    def __str__(self) -> str:
        return f"{self.name}"
    
class Manga(models.Model):

    title = models.CharField(max_length=255, verbose_name = 'Título')

    number_capthers = models.IntegerField(default = 0, verbose_name = 'Número de capítulos')

    author = models.ForeignKey(Author, on_delete = models.CASCADE, verbose_name = 'Author')

    synopsis = models.TextField(verbose_name = 'Sinopse')

    publish_date = models.DateField(verbose_name = 'Data de publicação')

    users = models.ManyToManyField(get_user_model(), through = 'Evaluation')

    cover = models.ImageField(upload_to = 'manga/%Y/%m/%d/', verbose_name = 'Capa')

    def __str__(self) -> str:
        return f'{self.title}'
    
class Evaluation(models.Model):

    manga = models.ForeignKey(Manga, on_delete = models.CASCADE, verbose_name = 'Mangá')

    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE, verbose_name = 'Usuário')

    rating = models.IntegerField(default = 0, verbose_name = 'Nota')

    comment = models.TextField(blank = True, null = True, verbose_name = 'Comentário')

    def __str__(self) -> str:
        return f'{self.user.username} avaliou "{self.manga.title}" como {self.rating}/10'