# from django.urls import path
# from .views import (
#     # custom_register,
#     user_profile,
#     user_list,
#     user_info_change,
#     my_page,
#     follow_user,
#     user_recommendation,
# )

# urlpatterns = [
    
    # path('register/', custom_register, name='register'), 
    # path('profile/', user_profile, name='profile'),       
    # path('users/', user_list, name='user_list'),         
    # path('profile/edit/', user_info_change, name='profile_edit'),  
    # path('mypage/', my_page, name='mypage'),              
    # path('follow/<int:pk>/', follow_user, name='follow'), 
    # path('recommendation/', user_recommendation, name='recommendation'),  
# ]

from django.urls import path
from .views import (
    user_profile,
    user_list,
    user_info_change,
    my_page,
    follow_user,
    user_recommendation,
    user_info,
)

urlpatterns = [
    # 사용자 프로필 조회 및 수정
    path('profile/', user_profile, name='user_profile'),

    # 사용자 전체 정보 조회 (관리자만 접근 가능)
    path('users/', user_list, name='user_list'),

    # 사용자 정보 수정
    path('profile/edit/', user_info_change, name='user_info_change'),

    # 마이페이지 조회
    path('mypage/', my_page, name='my_page'),

    # 팔로우/언팔로우
    path('follow/<int:pk>/', follow_user, name='follow_user'),

    # 상품 추천
    path('recommendation/', user_recommendation, name='user_recommendation'),

    # 사용자 목록 조회 및 추가 (GET/POST)
    path('userinfo/', user_info, name='user_info'),
]