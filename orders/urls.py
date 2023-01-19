from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name = 'cart'),
    path('cart/add/<int:product_id>', views.CardAddView.as_view(), name='cart_add'),
]