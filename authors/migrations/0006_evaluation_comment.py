# Generated by Django 4.1.7 on 2023-03-03 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0005_alter_manga_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Comentário'),
        ),
    ]
