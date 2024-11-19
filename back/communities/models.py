from django.db import models
from django.conf import settings

# Create your models here.
from django.db import models
from accounts.models import User
from django.db import models
from django.conf import settings

class Community(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE  # 커뮤니티 생성자
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"  # 작성자
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="articles")  # 소속 커뮤니티
    title = models.CharField(max_length=100)
    content = models.TextField()
    viewscount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"  # 작성자
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")  # 소속 게시글
    content = models.TextField()
    like = models.PositiveIntegerField(default=0)  # 댓글 좋아요 수
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"


class ArticleLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="article_likes"  # 좋아요 누른 사용자
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes")  # 좋아요 대상 게시글
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.article.title}"
