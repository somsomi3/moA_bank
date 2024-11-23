# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views
# from django.urls import path
# from .views import CardImageAPIView
# # # Router 설정 (ViewSet용)
# # router = DefaultRouter()
# # router.register(r'cards', views.CardViewSet, basename='card')
# # router.register(r'card-designs', views.CardDesignViewSet, basename='card-design')

# urlpatterns = [
#     # # ViewSet 라우팅
#     # path('', include(router.urls)),

#     # @api_view 기반 뷰 라우팅
#     # path('cards/list-create/', views.card_list_create, name='card-list-create'),
#     # path('cards/<int:card_id>/', views.card_detail, name='card-detail'),
#     # path('card-designs/list-create/', views.card_design_list_create, name='card-design-list-create'),
#     path('card-designs/<int:card_design_id>/', views.card_design_detail, name='card-design-detail'),
#     path('card-designs/generate_card/', views.generate_card, name='card-design-detail'),
#     path("generate-image/", CardImageAPIView.as_view(), name="generate_image"),
# ]
