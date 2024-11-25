from django.urls import path
from . import views
# from . import recommendation_views

urlpatterns = [
    path('deposits/', views.search_deposit_products, name='search_deposit_products'),
    path('savings/', views.search_saving_products, name='search_saving_products'),
    path('search/cards/', views.search_card_products, name='search_card_products'),
    # path('top_rate/', recommendation_views.top_rate, name='top_rate'),
    # path('top_rate_saving/', recommendation_views.top_rate_saving, name='top_rate_saving'),
    # path('recommend_deposit_products/', recommendation_views.recommend_deposit_products, name='recommend_deposit_products'),
    # path('recommend_saving_products/', recommendation_views.recommend_saving_products, name='recommend_saving_products'),
]
