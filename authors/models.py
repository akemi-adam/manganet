from django.db import models

class Author(models.Model):

    name = models.CharField(max_length=125)
    
    age = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name}"