from adminmanager import views
from django.urls import path

urlpatterns = [
    path('admin-login', views.admin_loogin, name= 'admin-login'),
    path('admin-logout', views.admin_logout, name= 'admin-logout'),
    path('admin-index', views.admin_index, name= 'admin-index'),
    path('admin-user', views.admin_user_list, name= 'admin-user'),
    path('block_user/<int:id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:id>/', views.unblock_user, name='unblock_user'),
    path('add_category', views.add_category, name= 'add_category'),
    path('category', views.Category_List, name= 'category'),
    path('edit_category/<int:id>/', views.Edit_Cat, name='edit_category'),
    path('soft_delete_category/<int:id>/', views.soft_delete_category, name='soft_delete_category'),
    path('undo_soft_delete_category/<int:id>/', views.undo_soft_delete_category, name='undo_soft_delete_category'),
    #product
    path('product_list', views.Product_list, name= 'product_list'),
    path('add_product', views.Add_Product, name= 'add_product'),
    path('edit_product/<int:id>/', views.Edit_Product, name='edit_product'),
    path('soft_delete_product/<int:product_id>/', views.soft_delete_product, name='soft_delete_product'),
    path('undo_soft_delete_product/<int:product_id>/', views.undo_soft_delete_product, name='undo_soft_delete_product'),




]