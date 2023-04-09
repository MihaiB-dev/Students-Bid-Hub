# Generated by Django 4.1.7 on 2023-03-29 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_bid_category_remove_bid_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('text', models.CharField(max_length=400)),
                ('startBid', models.PositiveIntegerField()),
                ('URL', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=200)),
                ('date_post', models.DateField()),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_bid', to='auctions.bid')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bid',
            name='category',
            field=models.ManyToManyField(blank=True, to='auctions.category'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='user_bid', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Auction_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_price', models.PositiveIntegerField()),
                ('last_bidder', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='auction_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]