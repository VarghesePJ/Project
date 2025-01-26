from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin, name='admin'),
    path('block/<int:user_id>/', views.blocking, name='block'),
    path('user_detail/<int:user_id>/',views.user_view, name='view'),
    path('category/', views.category, name='category'),
    path('category_create/',views.category_create, name='category_create'),
    path('category_view/<int:category_id>', views.category_view, name='category_view'),
    path('category_update/<int:category_id>', views.category_update, name='category_update'),
    path('category_delete/<int:category_id>', views.category_delete, name='category_delete'),
    path('product/', views.product, name='product'),
    path('product_create/',views.product_create, name='product_create'),
    path('product_view/<int:product_id>', views.Product_view, name='product_view'),
    path('product_update/<int:product_id>', views.product_update, name='product_update'),
    path('product_delete/<int:product_id>', views.product_delete, name='product_delete'),
    path('order/',views.order, name='order'),
]
