# Generated by Django 4.1.7 on 2023-03-03 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0003_evaluation_manga_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='cover',
            field=models.ImageField(default='manga.com', upload_to='', verbose_name='Capa'),
            preserve_default=False,
        ),
    ]
