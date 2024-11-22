from django.db import models
from django.conf import settings

class Community(models.Model):
    # ManyToMany 관계 설정(accounts의 모델에서 해서, 여기서는 적지 않아도됨. 
    # account에서 community_id가 있으면, 중개테이블은 굳이 필요없다.)
    # user = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL, related_name='joined_communities', blank=True
    # )
    name = models.CharField(max_length=100)
    decile = models.IntegerField(unique=True)  # 소득 분위 (1~10)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    # 게시글 모델
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=100)
    content = models.TextField()
    viewscount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    # 댓글 모델
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    like = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"


class ArticleLike(models.Model):
    # 게시글 좋아요 모델
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="article_likes"
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.article.title}"
