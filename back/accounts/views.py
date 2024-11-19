from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import User
from .serializers import (
    CustomRegisterSerializer,
    UserProfileSerializer,
    UserInfoSerializer,
    UserInfoChangeSerializer,
    MyPageSerializer,
    UserRecommendationSerializer,
)
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .serializers import UserProfileSerializer
from .models import User

# 사용자 프로필
# 사용자 상세정보
# 사용자 정보수정
# 마이페이지
# 상품추천-> community에서 하기


# 1. 회원가입
@api_view(['POST'])
def custom_register(request):
    serializer = CustomRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # 토큰 생성
        # token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "message": "회원가입 성공!",
            # "token": token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication, BasicAuthentication])
# def user_list(request):
#     if request.method == 'GET':
#         article = get_object_or_404()


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