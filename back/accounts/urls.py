from django.urls import path, include
from .views import (
    user_profile, user_list,
    user_info_change, my_page,
    follow_user, user_recommendation,
    user_info,
    # custom_register,
    save_profile_data,
)
from .views import CustomRegisterView  # 방금 생성한 CustomRegisterView 가져오기


urlpatterns = [
    # 기존 dj-rest-auth의 회원가입 엔드포인트 대체
    # path('dj-rest-auth/registration/', CustomRegisterView.as_view(), name='custom_registration'),

    # 사용자 프로필 조회 및 수정
    path('profile/', user_profile,),

    # 사용자 전체 정보 조회 (관리자만 접근 가능)
    path('users/', user_list,),

    # 사용자 정보 수정
    path('profile/edit/', user_info_change,),

    # 마이페이지 조회
    path('mypage/', my_page,),

    # 팔로우/언팔로우
    path('follow/<int:pk>/', follow_user, ),

    # 상품 추천
    path('recommendation/', user_recommendation,),

    # 사용자 목록 조회 및 추가 (GET/POST)
    path('userinfo/', user_info,),

    # 리포터 저장을 위한 url
    path('save_profile/<int:user_id>', save_profile_data, name='save_profile_data'),
]