from django.db import models
from accounts.models import User

class CardDesign(models.Model):
    image = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserMakingCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=255)
    card_image = models.CharField(max_length=255)
    # notification = models.TextField()
    # annual_fee = models.CharField(max_length=255)
    # base_performance = models.TextField()
    # base_performance_last = models.TextField(null=True, blank=True)
    # merit_summary = models.TextField()
    # card_design = models.ForeignKey(CardDesign, on_delete=models.CASCADE, related_name="cards")

    def __str__(self):
        return self.card_name
