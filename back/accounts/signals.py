from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# from allauth.account.signals import user_signed_up
# from django.dispatch import receiver

# @receiver(user_signed_up)
# def save_profile_data(request, user, **kwargs):
#     data = request.data
#     user.nickname = data.get("nickname", "")
#     user.gender = data.get("gender", "")
#     user.age = data.get("age", 0)
#     user.region = data.get("region", "")
#     user.main_bank = data.get("main_bank", "")
#     user.income = data.get("income", 0)
#     user.consume = data.get("consume", 0)
#     user.grade = data.get("grade", "")
#     user.job = data.get("job", "")
#     user.desire_period = data.get("desire_period", 0)
#     user.save()
