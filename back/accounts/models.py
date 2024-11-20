from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    # 본명
    nickname = models.CharField(max_length=100)

    # # 로그인시 입력받을 아이디 값으로, 고유한 값이어야하는 username
    username = models.CharField(max_length=50, unique=True)
    # name = models.CharField(max_length=50)
    
    # email = models.EmailField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=50, unique=True)
    profile_img = models.ImageField(upload_to='image/', default='image/user.png')
    # 현재 가지고 있는 상품
    financial_products = models.TextField(blank=True, null=True)
    
    # 매니저 수집자료
    age = models.IntegerField(blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)
    job = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    main_bank = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=10, blank=True, null=True)
    consume = models.IntegerField(blank=True, null=True)
    desire_period = models.IntegerField(blank=True, null=True)
    # 예금/적금량은 우리가 추천해줘야 한다. 
    # desire_amount_saving = models.IntegerField(blank=True, null=True)
    # desire_amount_deposit = models.IntegerField(blank=True, null=True)

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    


    # 관리자?
    # is_superuser = models.BooleanField(default=False)

    @staticmethod
    def clean_consume_and_period(user):
        user.consume = str(user.consume) if user.consume is not None else ""
        user.desire_period = str(user.desire_period) if user.desire_period is not None else ""
        user.save()
        
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


from allauth.account.adapter import DefaultAccountAdapter
class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        # nickname 
        nickname = data.get("nickname")
        
        email = data.get("email")
        financial_products = data.get("financial_products")
        age = data.get("age")
        income = data.get("income")
        job = data.get("job")
        gender = data.get("gender")
        grade = data.get("grade")
        main_bank = data.get("main_bank")
        region = data.get("region")
        consume = data.get("consume")
        desire_period = data.get("desire_period")

        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if gender:
            user_field(user, "gender", gender)

        if job:
            user_field(user, "job", job)
        if income:
            user_field(user, "income", income)
        if grade:
            user_field(user, "grade", grade)
        if main_bank:
            user_field(user, "main_bank", main_bank)
        if region:
            user_field(user, "region", region)
        if consume:
            user_field(user, "consume", consume)
        if desire_period:
            user_field(user, "desire_period", desire_period)

        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user