from django.db import models
from django.contrib.auth.models import AbstractUser
from communities.models import Community  # 커뮤니티 모델 import

class User(AbstractUser):
    # ForeignKey: 단일 커뮤니티와 연결
    community = models.ForeignKey(
        Community, on_delete=models.SET_NULL, null=True, blank=True, related_name="users_foreignkey"
    )
    
    # ManyToManyField: 여러 커뮤니티와 연결 가능
    communities = models.ManyToManyField(
        Community, related_name="members", blank=True
    )

    # 사용자 추가 필드
    nickname = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)

    # email = models.CharField(max_length=50, unique=True)
    profile_img = models.ImageField(upload_to='image/', default='image/user.png')
    financial_products = models.BooleanField(default=False)

    # 사용자 수집 정보
    age = models.IntegerField(default=0)
    income = models.IntegerField(default=0)
    job = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    main_bank = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=10, blank=True, null=True)
    consume = models.IntegerField(default=0)
    desire_period = models.IntegerField(default=0)

    # 사용자 팔로잉
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    USERNAME_FIELD = 'username'

    @staticmethod
    def clean_consume_and_period(user):
        user.consume = str(user.consume) if user.consume is not None else ""
        user.desire_period = str(user.desire_period) if user.desire_period is not None else ""
        user.save()


from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new User instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username
        data = form.cleaned_data

        # 사용자 정보 저장
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        # nickname 
        nickname = data.get("nickname")
        
        email = data.get("email")
        financial_products = data.get("financial_products")
        age = str(data.get("age"))
        income = str(data.get("income"))
        job = data.get("job")
        gender = data.get("gender")
        grade = data.get("grade")
        main_bank = data.get("main_bank")
        region = data.get("region")
        consume = str(data.get("consume"))
        desire_period = str(data.get("desire_period"))

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
        if age:
            user_field(user, "age", age)
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
        if financial_products:
            user_field(user, "financial_products", financial_products)
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

        # 소득 기반 커뮤니티 할당
        self.assign_user_to_community(user)
        return user
    def assign_user_to_community(self, user):
        """소득 분위에 따라 커뮤니티를 할당"""
        try:
            income_decile = self.calculate_income_decile(user.income)
            community, created = Community.objects.get_or_create(
                decile=income_decile,
                defaults={
                    'name': f"Community {income_decile}",
                    'description': f"Community for decile {income_decile}"
                }
            )
            user.community = community  # ForeignKey 필드 설정
            user.save()
            user.communities.add(community)  # ManyToMany 관계 추가
        except Exception as e:
            print(f"Error in assigning community: {e}")

    def calculate_income_decile(self, income):
        """소득 분위 계산"""
        try:
            income = int(income)*10000
        except (ValueError, TypeError):
            income = 0

        if income <= 2433469.5:
            return 1
        elif income <= 3104528.25:
            return 2
        elif income <= 3776786.875:
            return 3
        elif income <= 4494899.0:
            return 4
        elif income <= 5296783.5:
            return 5
        elif income <= 6215137.625:
            return 6
        elif income <= 7355015.5:
            return 7
        elif income <= 9051067.0:
            return 8
        elif income > 9051067.0:
            return 9
        return 10  # 상위 소득
