from django.urls import path
from . import views

urlpatterns = [
    path('',views.bill_detail, name='bill'),
    path('checkout/',views.checkout, name='checkout'),
    path('success/',views.success, name='success')
]