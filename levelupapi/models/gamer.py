from django.db import models
from django.contrib.auth.models import User


class Gamer(models.Model):

    # Relationship to the built-in User model which has name and email
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional address field to capture from the client
    bio = models.CharField(max_length=600)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'