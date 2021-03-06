# Generated by Django 3.2.12 on 2022-03-28 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advertisements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='status',
            field=models.TextField(choices=[('OPEN', 'Открыто'), ('CLOSED', 'Закрыто'), ('DRAFT', 'Черновик')], default='OPEN'),
        ),
        migrations.CreateModel(
            name='AdvertisementFavourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_user', to='advertisements.advertisement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_adv', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='advertisement',
            name='favourites',
            field=models.ManyToManyField(related_name='favourites', through='advertisements.AdvertisementFavourite', to=settings.AUTH_USER_MODEL),
        ),
    ]
