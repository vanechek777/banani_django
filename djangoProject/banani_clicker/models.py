from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    user_tg_id = models.IntegerField()
    user_picture = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    total_points = models.IntegerField(default=0)
    coins_per_sec = models.IntegerField(default=1)
    lvl = models.IntegerField(default=1)
    till_next_level = models.IntegerField(default=500)


class Cards(models.Model):
    id = models.IntegerField(primary_key=True)
    card_name = models.CharField(max_length=255)
    card_cost = models.IntegerField()
    card_add_points = models.IntegerField()
    card_rarity = models.CharField(max_length=255)
    card_lvl = models.IntegerField()


class CardHoldings(models.Model):
    user_id = models.IntegerField()
    card_id = models.IntegerField()
    card_lvl = models.IntegerField(default=0)
    card_new_cost = models.IntegerField()
    card_new_pnt_per_sec = models.IntegerField()
