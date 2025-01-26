from django.urls import path
from . import views

urlpatterns = [
    path('',views.Store, name='store'),
    path('product/<int:product_id>/',views.viewProduct, name='product')
]