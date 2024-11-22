from django.shortcuts import render

# Create your views here.

# 예적금 목록보기

# 예적금 검색한거 보기

from rest_framework.generics import ListAPIView
from data.models import DepositProducts, SavingProducts, Card
from .serializers import SearchProductSerializer, SearchSavingProductSerializer, SearchCardSerializer
from rest_framework.filters import SearchFilter


# 예금 관련 views.py
class SearchProductListView(ListAPIView):
    queryset = DepositProducts.objects.all()
    serializer_class = SearchProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['kor_co_nm', 'fin_prdt_nm']  # 검색 가능한 필드


# 적금 관련 views.py
class SearchSavingProductListView(ListAPIView):
    queryset = SavingProducts.objects.all()
    serializer_class = SearchSavingProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['kor_co_nm', 'fin_prdt_nm']  # 검색 가능한 필드

# 카드 검색 views.py
class SearchCardProductView(ListAPIView):
    queryset = Card.objects.all()
    serializer_class = SearchCardSerializer
    filter_backends = [SearchFilter]
    search_fields = ['card_name', 'annual_fee']  # 검색 가능한 필드
