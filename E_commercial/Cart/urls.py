from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='cart'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart, name='atc'),
    path('remove_from_cart/<int:product_id>/', views.remove_cart, name='remove'),
    path('update/<int:product_id>/<str:type>/', views.update_quantity, name='update'),

]