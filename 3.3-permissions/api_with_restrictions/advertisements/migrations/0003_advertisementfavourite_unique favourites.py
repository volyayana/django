# Generated by Django 3.2.12 on 2022-03-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0002_auto_20220328_2128'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='advertisementfavourite',
            constraint=models.UniqueConstraint(fields=('advertisement', 'user'), name='unique favourites'),
        ),
    ]
