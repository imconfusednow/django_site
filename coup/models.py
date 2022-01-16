from django.db import models

class players(models.Model):
    name = models.CharField(max_length=50, default="")
    game_id = models.CharField(max_length=50, default="")
    player_id = models.CharField(max_length=50, default="")
    sequence = models.IntegerField(default=0)
    turn = models.BooleanField(default=False)
    computer = models.BooleanField(default=False)
    coins = models.IntegerField(default=0)
    hand = models.CharField(max_length=50, default="")
