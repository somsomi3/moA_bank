

from rest_framework import serializers
# from .models import SearchProduct
from data.models import DepositProducts, SavingProducts, Card


# 예금상품 검색
class SearchProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = ['kor_co_nm', 'fin_prdt_nm', 'etc_note', 'join_member', 'join_way', 'spcl_cnd']  # 출력으로 보여줄 필드


# 적금상품 검색
class SearchSavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = ['kor_co_nm', 'fin_prdt_nm', 'join_member', 'etc_note', 'max_limit']   # 출력으로 보여줄 필드

# 카드 검색
class SearchCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_name', 'card_link', 'card_apply_link', 'card_image', 'annual_fee', 'merit_summary', ] # 보여줄 필드

