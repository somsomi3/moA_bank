from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Community, Article, Comment, ArticleLike
from .serializers import CommunitySerializer, ArticleSerializer, CommentSerializer, ArticleLikeSerializer
from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework import status
from .models import Community, Article, Comment, ArticleLike
from .serializers import CommunitySerializer, ArticleSerializer, ArticleListSerializer, CommentSerializer, ArticleLikeSerializer


# 커뮤니티 뷰셋
class CommunityViewSet(ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

# 게시글 뷰셋
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer



# 커뮤니티 목록 보기
@api_view(['GET'])
# 권한 drf설정
@permission_classes([IsAuthenticated])
def community_list(request):
    communities = get_list_or_404(Community)
    serializer = CommunitySerializer(communities, many=True)
    return Response(serializer.data)


# 커뮤니티 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_community(request):
    serializer = CommunitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # 커뮤니티 생성자를 현재 로그인한 사용자로 설정
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 커뮤니티 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_community(request, community_id):
    try:
        community = Community.objects.get(pk=community_id)
    except Community.DoesNotExist:
        return Response({"error": "Community not found."}, status=status.HTTP_404_NOT_FOUND)

    # 커뮤니티 생성자인지 확인
    if community.user != request.user:
        return Response(
            {"error": "You do not have permission to delete this community."},
            status=status.HTTP_403_FORBIDDEN,
        )

    community.delete()
    return Response({"message": "Community deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# 특정 커뮤니티의 게시판(articles) 목록 보기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def community_articles(request, community_id):
    try:
        community = Community.objects.get(pk=community_id)
    except Community.DoesNotExist:
        return Response({"error": "Community not found."}, status=status.HTTP_404_NOT_FOUND)

    articles = Article.objects.filter(community=community)
    serializer = ArticleListSerializer(articles, many=True)
    return Response({
        "community": CommunitySerializer(community).data,
        "articles": serializer.data,
    })


# 게시판에서 게시글 작성 및 게시글 목록 보기
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def article_create(request, community_id):
#     try:
#         community = Community.objects.get(pk=community_id)

        
#     except Community.DoesNotExist:
#         return Response({"error": "Community not found."}, status=status.HTTP_404_NOT_FOUND)
    
#     # if request.method == 'GET':
#     #     articles = Article.objects.filter(community=community)
#     #     serializer = ArticleListSerializer(articles, many=True)
#     #     return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         print(request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user, community=community)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_create(request, community_id):
    try:
        # community_id를 사용해 커뮤니티 가져오기
        community = Community.objects.get(pk=community_id)
    except Community.DoesNotExist:
        return Response({"error": "Community not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # GET 요청 처리: 커뮤니티의 게시글 목록 조회
    if request.method == 'GET':
        articles = Article.objects.filter(community=community)
        serializer = ArticleSerializer(articles, many=True)  # 게시글 목록 직렬화
        return Response(serializer.data)

    # POST 요청 처리: 게시글 생성
    if request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, community=community)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 특정 게시글 보기 및 댓글 작성/보기
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_detail_comment(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # 게시글 상세보기
        article_serializer = ArticleSerializer(article)
        comments = Comment.objects.filter(article=article)
        comment_serializer = CommentSerializer(comments, many=True)
        return Response({
            "article": article_serializer.data,
            "comments": comment_serializer.data,
        })

    elif request.method == 'POST':
        # 댓글 작성
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글 좋아요 추가/삭제
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

    like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)

    if not created:  # 이미 좋아요 상태라면 좋아요 삭제
        like.delete()
        return Response({"message": "Like removed."}, status=status.HTTP_200_OK)

    return Response({"message": "Article liked."}, status=status.HTTP_201_CREATED)