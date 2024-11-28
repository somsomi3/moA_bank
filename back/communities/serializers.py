from rest_framework import serializers
from .models import Community, Article, Comment, ArticleLike

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'
        read_only_fields = ('user', 'created_at')  # 로그인된 사용자가 자동으로 할당됨


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'created_at')  # 간단한 목록 출력용
        read_only_fields = ('created_at',)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'viewscount')  # 읽기 전용 필드


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'
#         read_only_fields = ('user', 'created_at', 'updated_at')  # 작성자와 생성/수정 날짜는 읽기 전용
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'article', 'like', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'article', 'like', 'created_at', 'updated_at']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("댓글 내용은 비어 있을 수 없습니다.")
        return value

class ArticleLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleLike
        fields = '__all__'
        read_only_fields = ('user', 'created_at')  # 좋아요한 사용자와 생성 시간은 읽기 전용

