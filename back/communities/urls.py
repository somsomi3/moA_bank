# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import CommunityViewSet, ArticleViewSet, create_comment, like_article

# # ViewSet 기반 URL 등록
# router = DefaultRouter()
# router.register(r'communities', CommunityViewSet, basename='community')
# router.register(r'articles', ArticleViewSet, basename='article')

# urlpatterns = [
#     path('', include(router.urls)),  # 커뮤니티 및 게시글 URL
#     path('articles/<int:article_id>/comments/', create_comment, name='create_comment'),  # 댓글 추가
#     path('articles/<int:article_id>/like/', like_article, name='like_article'),  # 게시글 좋아요
# ]

# from django.urls import path
# from .views import community_list, community_articles, article_list_create, article_detail_comment

# urlpatterns = [
#     # 커뮤니티 목록 보기
#     path('communities/', community_list, name='community_list'),

#     # 특정 커뮤니티의 게시판 보기
#     path('communities/<int:community_id>/articles/', community_articles, name='community_articles'),

#     # 게시판에서 게시글 작성 및 목록 보기
#     path('communities/<int:community_id>/articles/list/', article_list_create, name='article_list_create'),

#     # 게시글 상세 보기 및 댓글 작성/보기
#     path('articles/<int:article_id>/', article_detail_comment, name='article_detail_comment'),
# ]

from django.urls import path
from .views import (
    community_list,
    create_community,
    delete_community,
    community_articles,
    article_create,
    article_detail_comment,
    like_article,
)

urlpatterns = [
    path('', community_list, ),
    path('create/', create_community,),
    path('<int:community_id>/delete/', delete_community, ),
    path('<int:community_id>/articles/list/', community_articles, ),
    path('<int:community_id>/articles/create/', article_create,),
    path('articles/<int:article_id>/', article_detail_comment,),
    path('articles/<int:article_id>/like/', like_article, ),
]
