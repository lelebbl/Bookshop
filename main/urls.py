from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
     path('', views.popular_list, name='popular_list'),
     path('shop/', views.product_list, name='product_list'),
     path('shop/<slug:slug>/', views.product_detail,
         name='product_detail'),
     path('shop/category/<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
     path('admin-panel/', views.admin_panel, name='admin_panel'),
      path('users/', include('users.urls', namespace='users')),

     # Category
     path('admin-panel/category/create/', views.category_create, name='category_create'),
     path('admin-panel/category/<int:pk>/update/', views.category_update, name='category_update'),
     path('admin-panel/category/<int:pk>/delete/', views.category_delete, name='category_delete'),

     # Product
     path('admin-panel/product/create/', views.product_create, name='product_create'),
     path('admin-panel/product/<int:pk>/update/', views.product_update, name='product_update'),
     path('admin-panel/product/<int:pk>/delete/', views.product_delete, name='product_delete'),
]
