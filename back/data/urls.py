# from django.urls import path
# from . import views
# from django.conf.urls.static import static
# from django.conf import settings
# from django.contrib import admin
# app_name = 'articles'
# urlpatterns = [ 
#     # path('index/', views.index ),
#     path('savedata/', views.savedata_view, name='savedata'),
#     path('savedata2/', views.savedata_view2, name = 'savedata2'),
#     path('savedata3/', views.savedata_view3, name = 'savedata3'),
#     path('savedata4/', views.savedata_view4, name = 'savedata4'),
#     path('save-deposit-products/', views.save_deposit_products),
#     # path('deposit-products/',views.deposit_products),
#     # path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),
#     # path('deposit-products/top_rate/',views.top_rate),
#     path('save/', views.save_card_data, name = 'save_card_data' ),
#     # path('get_recommended_products/', views.get_recommended_products),
#     path('save-saving-products/', views.save_saving_products),
#     # path('saving-products/',views.saving_products),
#     # path('saving-product-options/<str:fin_prdt_cd>/', views.saving_product_options),
#     # path('saving-products/top_rate/',views.top_rate2),
#     # path('get_recommended_products2/', views.get_recommended_products2),
#     path('admin/', admin.site.urls),
#     path('api/recommend/', views.recommend, name='recommend'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#============gpt코드
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

app_name = 'articles'

urlpatterns = [ 
    path('savedata/', views.savedata_view, name='savedata'),
    path('savedata2/', views.savedata_view2, name='savedata2'),
    path('savedata3/', views.savedata_view3, name='savedata3'),
    path('savedata4/', views.savedata_view4, name='savedata4'),
    path('savedata5/', views.savedata_view5, name='savedata5'),
    path('savedata6/', views.savedata_view6, name='savedata6'),
    path('save-deposit-products/', views.save_deposit_products),
    path('save/', views.save_card_data, name='save_card_data'),
    path('save-saving-products/', views.save_saving_products),
    path('admin/', admin.site.urls),
    # path('api/recommend/', views.RecommendView.as_view(), name='recommend'),  # Updated to use the new RecommendView class
    path('form/', views.input_form_view, name='input_form'),  # Added URL pattern
    # path('recommend/', views.get_recommendations, name='recommend'),
    path('recommend_view/<int:user_id>/', views.recommend_view, name='recommend_view'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

