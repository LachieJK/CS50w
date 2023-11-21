# Generated by Django 4.2.5 on 2023-11-17 10:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listings_comments_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='watched_by',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]