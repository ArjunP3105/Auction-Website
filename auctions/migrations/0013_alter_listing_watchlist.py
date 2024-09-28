# Generated by Django 5.1 on 2024-09-16 16:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_remove_listing_wishlist_listing_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
