# Generated by Django 4.1.6 on 2023-02-07 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='gamer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='game_creator', to='levelupapi.gamer'),
        ),
    ]
