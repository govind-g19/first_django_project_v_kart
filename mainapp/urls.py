from mainapp import views
from django.urls import path

urlpatterns = [
    path('index',views.index, name='index'),
    path('base', views.base, name= 'base'),
    path('shop', views.shop, name= 'shop'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
]