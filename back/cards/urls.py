from django.urls import path
from .views import (
    CardListCreateView,
    CardDetailView,
    CardDesignListCreateView,
    CardDesignDetailView,
)

urlpatterns = [
    path('cards/', CardListCreateView.as_view(), name='card-list'),
    path('cards/<int:pk>/', CardDetailView.as_view(), name='card-detail'),
    path('card-designs/', CardDesignListCreateView.as_view(), name='card-design-list'),
    path('card-designs/<int:pk>/', CardDesignDetailView.as_view(), name='card-design-detail'),
]
