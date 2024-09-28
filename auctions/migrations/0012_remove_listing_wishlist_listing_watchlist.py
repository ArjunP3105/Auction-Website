# Generated by Django 5.1 on 2024-09-16 14:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_listing_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='wishlist',
        ),
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(null=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
