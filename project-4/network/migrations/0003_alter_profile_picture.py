# Generated by Django 4.2.5 on 2023-12-23 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_profile_post_following_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='profile-pics/default.jpg', upload_to='profile-pics'),
        ),
    ]
