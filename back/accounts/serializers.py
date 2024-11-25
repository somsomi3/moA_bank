
 # accounts/serializers.py
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User, Report

class CustomRegisterSerializer(RegisterSerializer):    
    # def create(self, validated_data):
    #     # 기본 사용자 생성 로직 실행
    #     user = super().create(validated_data)
    #     return user  # 저장된 사용자 객체 반환

    # 필요한 필드들을 추가합니다.
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255
    )
    username = serializers.CharField(
        required=True,
        max_length=50
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        max_length=300
    )
    profile_img = serializers.ImageField(
        required=False
    )
    financial_products = serializers.CharField(
        required=False,
        allow_blank=True
    )
    age = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    income = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    job = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=50
    )
    gender = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=10
    )
    grade = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=10
    )
    main_bank = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=10
    )
    region = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=10
    )
    consume = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    desire_period = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'email': self.validated_data.get('email', ''),
            'profile_img': self.validated_data.get('profile_img', ''),
            'financial_products': self.validated_data.get('financial_products', ''),

            'age': self.validated_data.get('age', ''),
            'income': self.validated_data.get('income', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'job' : self.validated_data.get('job', ''),
            'gender' : self.validated_data.get('gender', ''),
            'grade' : self.validated_data.get('grade', ''),
            'main_bank' : self.validated_data.get('main_bank', ''),
            'region' : self.validated_data.get('region', ''),
            'consume' : self.validated_data.get('consume', ''),
            'desire_period' : self.validated_data.get('desire_period', ''),
        }


# userdetail serializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
UserModel = get_user_model()
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        # if hasattr(UserModel, 'first_name'):
        #     extra_fields.append('first_name')
        # if hasattr(UserModel, 'last_name'):
        #     extra_fields.append('last_name')
        if hasattr(UserModel, 'nickname'):
            extra_fields.append('nickname')    

        # 없어도 db에 저장 됨.
        if hasattr(UserModel, 'gender'):  # gender 필드 추가
            extra_fields.append('gender')

        if hasattr(UserModel, 'job'):
            extra_fields.append('job') 
        
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)




    def save(self, request):
        # 기존 save 메서드 호출
        user = super().save(request)
        # 커스텀 필드 저장
        user.name = self.validated_data.get('name', '')
        user.save()
        return user

# from dj_rest_auth.registration.serializers import RegisterSerializer
# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class CustomRegisterSerializer(RegisterSerializer):
#     username = serializers.CharField(required=True)
#     name = serializers.CharField(required=True)
#     age = serializers.IntegerField(required=False)
#     income = serializers.FloatField(required=False)
#     job = serializers.CharField(required=False)
#     gender = serializers.CharField(required=False)
#     grade = serializers.CharField(required=False)
#     main_bank = serializers.CharField(required=False)
#     region = serializers.CharField(required=False)
#     consume = serializers.FloatField(required=False)
#     desire_period = serializers.IntegerField(required=False)
#     financial_product = serializers.CharField(required=False)

#     def save(self, request):
#         user = super().save(request)
#         # 추가 필드 저장
#         user.name = self.validated_data.get('name', '')
#         user.age = self.validated_data.get('age', None)
#         user.income = self.validated_data.get('income', None)
#         user.job = self.validated_data.get('job', '')
#         user.gender = self.validated_data.get('gender', '')
#         user.grade = self.validated_data.get('grade', '')
#         user.main_bank = self.validated_data.get('main_bank', '')
#         user.region = self.validated_data.get('region', '')
#         user.consume = self.validated_data.get('consume', None)
#         user.desire_period = self.validated_data.get('desire_period', None)
#         user.financial_product = self.validated_data.get('financial_product', '')
#         user.save()
#         return user






# 2. 사용자 프로필 (UserProfileSerializer)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'username', 'nickname', 'email', 'following')

# 3. 사용자 전체 정보 조회 (UserInfoSerializer)
class UserInfoSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'username', 'name', 'following')

# 4. 사용자 정보 수정 (UserInfoChangeSerializer)
class UserInfoChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'profile_img', 'email', 'age', 'income', 'consume', 'job',
            'gender', 'grade', 'main_bank', 'region', 'desire_period'
        ]

# 5. 마이페이지 조회 (MyPageSerializer)
class MyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'name', 'profile_img', 'email', 'age', 'income',
            'consume', 'job', 'gender', 'main_bank', 'region', 'financial_products'
        ]
        read_only_fields = ('id', 'username', 'name')

# 6. 상품 추천 관련 직렬화 (UserRecommendationSerializer)
class UserRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'age', 'income', 'consume', 'job',
            'main_bank', 'region', 'gender', 'grade'
        ]


# 레포트 관련 Serializer: 위의 마이페이지에 레포트를 저장하는 
# 것이 목적임
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'