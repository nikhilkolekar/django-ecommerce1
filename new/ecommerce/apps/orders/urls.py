from django.urls import path
from .views import order_summary, add_to_cart

urlpatterns = [
    path('summary/', order_summary, name='order_summary'),
    path('add/<int:pk>/', add_to_cart, name='add_to_cart'),
]
