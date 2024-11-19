from rest_framework import serializers
from .models import User

from dj_rest_auth.registration.serializers import RegisterSerializer

# 다른 위치에서 serializer 가져오기
# from financial_instruments.serializers import ContractDepositSerializer, ContractSavingSerializer



# 입력 데이터를 받아 , 모델필드에 맞추어, serializer을 진행하고 보여줄거다.
# 1. 회원가입 (CustomRegisterSerializer)
class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100
    )
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=False)

    def get_cleaned_data(self):
        # 기본 필드와 커스텀 필드 데이터를 결합하여 반환
        data = super().get_cleaned_data()
        data['name'] = self.validated_data.get('name', '')
        return data

# 2. 사용자 프로필 (UserProfileSerializer)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_img', 'id', 'username', 'name', 'email', 'age', 'income', 'job')
        read_only_fields = ('id', 'username', 'name', 'email', 'following')

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


