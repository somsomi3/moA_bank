from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    # 로그인시 입력받을 아이디 값으로, 고유한 값이어야하는 username
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    
    email = models.EmailField(max_length=300, blank=True, null=True)
    profile_img = models.ImageField(upload_to='image/', default='image/user.png')
    # 현재 가지고 있는 상품
    financial_products = models.TextField(blank=True, null=True)
    
    # 매니저 수집자료
    age = models.IntegerField(blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)
    job = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)
    main_bank = models.CharField(max_length=10)
    region = models.CharField(max_length=10)
    consume = models.IntegerField(blank=True, null=True)
    desire_period = models.IntegerField(blank=True, null=True)
    # 예금/적금량은 우리가 추천해줘야 한다. 
    # desire_amount_saving = models.IntegerField(blank=True, null=True)
    # desire_amount_deposit = models.IntegerField(blank=True, null=True)

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    


    # 관리자?
    # is_superuser = models.BooleanField(default=False)

    


    USERNAME_FIELD = 'username'

# # 커뮤니티 앱에서 배너/ Article 분류에 사용됨.
# class CustomUser(AbstractUser):
#     income_bracket = models.CharField(
#         max_length=20,
#         choices=[
#             ('low', 'Low Income'),
#             ('middle', 'Middle Income'),
#             ('high', 'High Income'),
#         ],
#         default='middle'
#     )
