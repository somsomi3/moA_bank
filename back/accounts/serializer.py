from rest_framework import serializers
from .models import User

from dj_rest_auth.registration.serializers import RegisterSerializer

# 다른 위치에서 serializer 가져오기
# from financial_instruments.serializers import ContractDepositSerializer, ContractSavingSerializer



# 입력 데이터를 받아 , 모델필드에 맞추어, serializer을 진행하고 보여줄거다.

# 1. 회원가입
class CustomRegisterSerializer(RegisterSerializer):
    # 추가할 필드들을 정의합니다.
    username = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100
    )
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=False)
   
    
    # def

# 2. userprofile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_img', 'id', 'username', 'name', 'email', 'age', 'money', 'job')
        read_only_fields = ('id','username', 'name', 'following',)


# 3. userinfo
class UserInfoSerializer(serializers.ModelSerializer):
        profile_img = serializers.ImageField(use_url=True)
        
        class Meta:
            model = User
            fields = '__all__'
            read_only_fields = ('id','username', 'name', 'following',)

# 4. userinfochange

# 5. mypage

# 7. 상품 추천관련  직렬화

class UserRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'age', 'income', 'consume', 'job',
            'main_bank', 'region', 'gender', 'grade'
        ]

# 6. 리포터 불러오기=> 프론트?






