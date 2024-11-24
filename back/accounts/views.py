from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import User,Report
from .serializers import (
    # CustomRegisterSerializer,
    UserProfileSerializer,
    UserInfoSerializer,
    UserInfoChangeSerializer,
    MyPageSerializer,
    UserRecommendationSerializer,
    ReportSerializer
)
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .serializers import UserProfileSerializer
from .models import User


from dj_rest_auth.registration.views import RegisterView

# CustomRegisterView 정의
class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # # 숫자형 데이터를 문자열로 변환 (임시 처리)
        # if isinstance(data.get("age"), int):
        #     data["age"] = str(data["age"])

        request._data = data  # 수정된 데이터를 request에 덮어쓰기
        return super().create(request, *args, **kwargs)
    
# 1. 사용자 정보 조회
@api_view(['GET',])
def user_info(request):
    if request.method == 'GET':
        users = get_list_or_404(User)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



# 2. 사용자 프로필 조회/수정
@api_view(['GET', 'PUT'])
def user_profile(request):
    if not request.user.is_authenticated:
        return Response({"detail": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 3. 사용자 전체 정보 조회 (관리자만 접근 가능)
@api_view(['GET'])
def user_list(request):
    if not request.user.is_staff:
        return Response({"detail": "관리자 권한이 필요합니다."}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.all()
    serializer = UserInfoSerializer(users, many=True)
    return Response(serializer.data)

# 4. 사용자 정보 수정
@api_view(['PUT'])
def user_info_change(request):
    if not request.user.is_authenticated:
        return Response({"detail": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = UserInfoChangeSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "사용자 정보가 수정되었습니다."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 5. 마이페이지 정보 조회
@api_view(['GET'])
def my_page(request):
    if not request.user.is_authenticated:
        return Response({"detail": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = MyPageSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 6. 팔로우/언팔로우
@api_view(['POST'])
def follow_user(request, pk):
    if not request.user.is_authenticated:
        return Response({"detail": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    target_user = get_object_or_404(User, pk=pk)
    if target_user == request.user:
        return Response({"message": "자기 자신은 팔로우할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    if target_user in request.user.following.all():
        request.user.following.remove(target_user)
        return Response({"message": "언팔로우 완료!"}, status=status.HTTP_200_OK)
    else:
        request.user.following.add(target_user)
        return Response({"message": "팔로우 성공!"}, status=status.HTTP_200_OK)

# 7. 상품 추천
@api_view(['GET'])
def user_recommendation(request):
    if not request.user.is_authenticated:
        return Response({"detail": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = UserRecommendationSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.db import transaction
import json

# @receiver(user_signed_up)
# @csrf_exempt
# def save_profile_data(request, user, **kwargs):
#     """
#     회원가입 후 추가 데이터를 User 모델 또는 UserProfile에 저장.
#     """
#     try:
#         if request.content_type == 'application/json':
#             data = json.loads(request.body)
#         else:
#             data = request.POST

#         print("Received data:", data)

#         # Transaction으로 데이터 저장
#         with transaction.atomic():
#             user.nickname = data.get("nickname", "")
#             user.gender = data.get("gender", "")
#             user.age = int(data.get("age", 0))
#             user.region = data.get("region", "")
#             user.main_bank = data.get("main_bank", "")
#             user.income = float(data.get("income", 0))
#             user.consume = float(data.get("consume", 0))
#             user.grade = data.get("grade", "")
#             user.job = data.get("job", "")
#             user.desire_period = int(data.get("desire_period", 0))
#             user.save()

#     except Exception as e:
#         print(f"Error saving profile data: {e}")


#         @receiver(user_signed_up)
# def save_profile_data(sender, user, request, **kwargs):
#     """
#     회원가입 후 추가 데이터를 User 모델 또는 UserProfile에 저장.
#     """
#     try:
#         # 요청 데이터 가져오기
#         if request.content_type == 'application/json':
#             data = json.loads(request.body.decode('utf-8'))  # request.body는 바이트로 반환되므로 decode 필요
#         else:
#             data = request.POST.dict()

#         print("Received data:", data)

#         # Transaction으로 데이터 저장
#         with transaction.atomic():
#             user.nickname = data.get("nickname", "")
#             user.gender = data.get("gender", "")
#             user.age = int(data.get("age", 0))
#             user.region = data.get("region", "")
#             user.main_bank = data.get("main_bank", "")
#             user.income = float(data.get("income", 0))
#             user.consume = float(data.get("consume", 0))
#             user.grade = data.get("grade", "")
#             user.job = data.get("job", "")
#             user.desire_period = int(data.get("desire_period", 0))
#             user.save()

#     except Exception as e:
#         print(f"Error saving profile data: {e}")
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def save_profile_data(request):
    try:
        data = request.data  # DRF의 request.data 사용
        print("Received data:", data)

        # 사용자 데이터 저장
        user = request.user
        with transaction.atomic():
            user.nickname = data.get("nickname", "")
            user.gender = data.get("gender", "")
            user.age = int(data.get("age", 0))
            user.region = data.get("region", "")
            user.main_bank = data.get("main_bank", "")
            user.income = float(data.get("income", 0))
            user.consume = float(data.get("consume", 0))
            user.grade = data.get("grade", "")
            user.job = data.get("job", "")
            user.desire_period = int(data.get("desire_period", 0))
            user.save()

        return Response({"message": "Profile saved successfully!"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_profile_data(request):
    # 요청 데이터에서 사용자 정보를 가져옵니다.
    user = request.user
    data = request.data

    # 기존 리포트가 있는지 확인합니다.
    report, created = Report.objects.get_or_create(user=user)

    # 리포트 데이터를 업데이트합니다.
    serializer = ReportSerializer(instance=report, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "리포트가 성공적으로 저장되었습니다.",
            "report": serializer.data
        }, status=201)
    else:
        return Response(serializer.errors, status=400)