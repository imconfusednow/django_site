from django.db import models

class players(models.Model):
    name = models.CharField(max_length=50, default="")
    game_id = models.ForeignKey("games", on_delete=models.SET(None), null=True)
    player_id = models.CharField(max_length=50, default="")
    turn = models.BooleanField(default=False)
    computer = models.BooleanField(default=False)
    coins = models.IntegerField(default=0)
    hand = models.CharField(max_length=50, default="")
    challenged_by = models.CharField(max_length=50, default="")
    blocked_by = models.CharField(max_length=50, default="")
    sequence = models.IntegerField(default=0)
    alive = models.BooleanField(default=True)

class games(models.Model):
    name = models.CharField(max_length=50, default="")
    started = models.BooleanField(default=False)

class decks(models.Model):
    game_id = models.ForeignKey("games", on_delete=models.CASCADE)
    card_type = models.CharField(max_length=10, default="")
