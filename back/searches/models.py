# from django.db import models

# # Create your models here.

# from django.db import models

# class SearchProduct(models.Model):
#     name = models.CharField(max_length=255)  # 상품명
#     bank = models.CharField(max_length=255)  # 은행 이름
#     interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # 이자율
#     description = models.TextField(blank=True)  # 상품 설명
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

#  모델은 데이터 앱에서 