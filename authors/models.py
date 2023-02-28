from django.db import models
from django.contrib.auth import get_user_model

class Author(models.Model):

    name = models.CharField(max_length=125)
    
    age = models.IntegerField()

    user_id = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"
    
class Manga(models.Model):


    title = models.CharField(max_length=255)

    number_capthers = models.IntegerField(default = 0)

    author = models.ForeignKey(Author, on_delete = models.CASCADE)

    synopsis = models.TextField()

    publish_date = models.DateField()

    def __str__(self) -> str:
        return f'{self.title}'