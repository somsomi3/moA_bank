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
    user_decile = models.IntegerField(default=0)
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
    # def assign_user_to_community(self, user):
    #     """소득 분위에 따라 커뮤니티를 할당"""
    #     try:
    #         income_decile = self.calculate_income_decile(user.income)
    #         community, created = Community.objects.get_or_create(
    #             decile=income_decile,
    #             defaults={
    #                 'name': f"Community {income_decile}",
    #                 'description': f"Community for decile {income_decile}"
    #             }
    #         )
    #         user.community = community  # ForeignKey 필드 설정
    #         user.save()
    #         user.communities.add(community)  # ManyToMany 관계 추가
    #     except Exception as e:
    #         print(f"Error in assigning community: {e}")
    def assign_user_to_community(self, user):
        """소득 분위에 따라 커뮤니티를 할당"""
        try:
            # 사용자 소득 분위 계산
            income_decile = self.calculate_income_decile(user.income)
            print(f"Calculated decile: {income_decile} for user: {user.id}")

            # decile에 따라 커뮤니티 ID 결정
            if 1 <= income_decile <= 4:
                community_id = 1
            elif 5 <= income_decile <= 8:
                community_id = 2
            elif 9 <= income_decile <= 10:
                community_id = 3
            else:
                print("Invalid decile. Assigning to default community.")
                community_id = None  # 기본 커뮤니티 ID가 없다면 None 처리

            # 커뮤니티 가져오기
            community = Community.objects.get(id=community_id)
            print(f"Assigning user {user.id} to community {community.name}")

            # ForeignKey 또는 ManyToMany 관계 설정
            user.user_decile = income_decile
            user.community = community  # ForeignKey 관계일 경우
            user.save()
        except Community.DoesNotExist:
            print(f"Community with ID {community_id} does not exist.")
            # 필요한 경우, 기본 커뮤니티로 설정
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
    

# 1. HelloView에서 생성된 리포트를 db와 연결하여, 리포트를 저장하고, 
# 2. 마이페이지에서 출력하게끔 만드는 첫순서
# 1-1 모델 만들기
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="report")  # 사용자와 연결
    income_analysis = models.TextField()
    income_decile = models.CharField(max_length=50)
    spending_analysis = models.TextField()
    job_analysis = models.TextField()
    grade_analysis = models.TextField()
    card_recommendations = models.JSONField(default=list, null=True, blank=True)  # 배열 저장
    deposit_recommendations = models.JSONField(default=list, null=True, blank=True)  # 배열 저장
    saving_recommendations = models.JSONField(default=list, null=True, blank=True)  # 배열 저장
    tax_refund_estimation = models.JSONField(default=list, null=True, blank=True)  # 배열 저장
    created_at = models.DateTimeField(auto_now_add=True)
    bank = models.TextField()
    
    
    def __str__(self):
        return f"{self.user.username}'s Report"
    

