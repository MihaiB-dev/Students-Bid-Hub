# Generated by Django 4.1.7 on 2023-04-02 19:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_remove_comment_bid_comment_auction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_post',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]