from django.urls import path
from .views import SearchProductListView, SearchSavingProductListView, SearchCardProductView

urlpatterns = [
    path('search/deposit/', SearchProductListView.as_view(), name='deposit-product-search'),
    path('search/saving/', SearchSavingProductListView.as_view(), name='deposit-saving-product-search'),
    path('search/cards/', SearchCardProductView.as_view(), name='card-search'),
]
