from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    date_of_event = models.DateTimeField()
    location = models.CharField(max_length=100)
    game = models.ForeignKey("Game", default=1, on_delete=models.CASCADE, related_name='game_events')
    host = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='event_host')
    gamer = models.ManyToManyField("Gamer", default=1)