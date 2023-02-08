# Generated by Django 4.1.6 on 2023-02-07 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0002_game_gamer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='gamer',
        ),
        migrations.RemoveField(
            model_name='event',
            name='host',
        ),
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.ManyToManyField(related_name='event_host', to='levelupapi.gamer'),
        ),
    ]
