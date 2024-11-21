from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Card, CardDesign
from .serializers import CardSerializer, CardDesignSerializer

# # Card ViewSet
# class CardViewSet(ModelViewSet):
#     queryset = Card.objects.all()
#     serializer_class = CardSerializer


# # CardDesign ViewSet
# class CardDesignViewSet(ModelViewSet):
#     queryset = CardDesign.objects.all()
#     serializer_class = CardDesignSerializer


# 카드 목록 조회 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def card_list_create(request):
    if request.method == 'GET':
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 카드 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def card_detail(request, card_id):
    card = get_object_or_404(Card, pk=card_id)

    if request.method == 'GET':
        serializer = CardSerializer(card)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CardSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        card.delete()
        return Response({"message": "Card deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# 카드 디자인 목록 조회 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def card_design_list_create(request):
    if request.method == 'GET':
        card_designs = CardDesign.objects.all()
        serializer = CardDesignSerializer(card_designs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CardDesignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 카드 디자인 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def card_design_detail(request, card_design_id):
    card_design = get_object_or_404(CardDesign, pk=card_design_id)

    if request.method == 'GET':
        serializer = CardDesignSerializer(card_design)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CardDesignSerializer(card_design, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        card_design.delete()
        return Response({"message": "Card design deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
