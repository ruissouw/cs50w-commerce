# Generated by Django 5.0.4 on 2024-05-13 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_bid_removed_comment_removed_watchlist_removed"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
