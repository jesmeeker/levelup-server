from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=155)
    description = models.CharField(max_length=600)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='game')
    min_player = models.IntegerField()
    max_player = models.IntegerField()
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, default=1, related_name='game_creator')