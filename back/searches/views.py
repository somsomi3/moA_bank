# from django.shortcuts import render
# from rest_framework.generics import ListAPIView
# from data.models import DepositProducts, SavingProducts, Card
# from .serializers import SearchProductSerializer, SearchSavingProductSerializer, SearchCardSerializer
# from data.serializers import SavingProductSerializer
# from rest_framework.filters import SearchFilter


# # 예금 관련 views.py
# class SearchProductListView(ListAPIView):
#     queryset = DepositProducts.objects.all()
#     serializer_class = SearchProductSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['kor_co_nm', 'fin_prdt_nm']  # 검색 가능한 필드


# # 카드 검색 views.py
# class SearchCardProductView(ListAPIView):
#     queryset = Card.objects.all()
#     serializer_class = SearchCardSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['card_name', 'annual_fee']  # 검색 가능한 필드


# # 예금의 product와 options를 모두 가져오는 views.py
# class SearchProductsAPI(ListAPIView):
#     queryset = DepositProducts.objects.prefetch_related('depositoptions_set').all()
#     serializer_class = SearchProductSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['kor_co_nm', 'fin_prdt_nm']  # 검색 가능한 필드



# # 적금의 product와 options를 모두 가져오는 views.py
# class SearchSavingProductsAPI(ListAPIView):
#     queryset = SavingProducts.objects.prefetch_related('savingoptions_set').all()
#     serializer_class = SearchSavingProductSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['kor_co_nm', 'fin_prdt_nm']  # 검색 가능한 필드


# 함수 방식으로 상품 검색 views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from data.models import DepositProducts, SavingProducts, Card
from .serializers import SearchProductSerializer, SearchSavingProductSerializer, SearchCardSerializer


@api_view(['GET'])
def search_deposit_products(request):
    """
    예금 상품 검색 뷰
    """
    search_query = request.GET.get('search', '').strip()  # 검색어 가져오기
    queryset = DepositProducts.objects.all()
    
    if search_query:
        queryset = queryset.filter(
            fin_prdt_nm__icontains=search_query) | queryset.filter(
            kor_co_nm__icontains=search_query
        )

    serializer = SearchProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_saving_products(request):
    """
    적금 상품 검색 뷰
    """
    search_query = request.GET.get('search', '').strip()  # 검색어 가져오기
    queryset = SavingProducts.objects.all()
    
    if search_query:
        queryset = queryset.filter(
            fin_prdt_nm__icontains=search_query) | queryset.filter(
            kor_co_nm__icontains=search_query
        )

    serializer = SearchSavingProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_card_products(request):
    """
    카드 상품 검색 뷰
    """
    search_query = request.GET.get('search', '').strip()  # 검색어 가져오기
    queryset = Card.objects.all()
    
    if search_query:
        queryset = queryset.filter(
            card_name__icontains=search_query) | queryset.filter(
            annual_fee__icontains=search_query
        )

    serializer = SearchCardSerializer(queryset, many=True)
    return Response(serializer.data)

