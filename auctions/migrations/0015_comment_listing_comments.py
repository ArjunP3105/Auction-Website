# Generated by Django 5.1 on 2024-09-17 14:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_listing_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=100000000)),
                ('user', models.ManyToManyField(null=True, related_name='user_comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='comments',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.comment'),
        ),
    ]
