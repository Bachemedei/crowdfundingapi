# Generated by Django 3.0.8 on 2020-09-24 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.URLField(default='https://image.freepik.com/free-vector/cat-paw-footprint_71328-557.jpg'),
            preserve_default=False,
        ),
    ]
