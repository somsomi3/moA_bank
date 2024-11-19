from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Card, CardDesign
from .serializers import CardSerializer, CardDesignSerializer

class CardListCreateView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardDesignListCreateView(generics.ListCreateAPIView):
    queryset = CardDesign.objects.all()
    serializer_class = CardDesignSerializer


class CardDesignDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CardDesign.objects.all()
    serializer_class = CardDesignSerializer
