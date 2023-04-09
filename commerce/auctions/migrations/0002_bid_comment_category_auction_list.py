# Generated by Django 4.1.7 on 2023-03-27 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('text', models.CharField(max_length=400)),
                ('startBid', models.PositiveIntegerField()),
                ('URL', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=200)),
                ('date_post', models.DateField()),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_bid', to='auctions.bid')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('bids', models.ManyToManyField(blank=True, related_name='categories', to='auctions.bid')),
            ],
        ),
        migrations.CreateModel(
            name='Auction_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_price', models.PositiveIntegerField()),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction_bid', to='auctions.bid')),
            ],
        ),
    ]
