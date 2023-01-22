from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CardAddForm

class CartView(View):

    def get(self, request):
        return render(request, 'orders/cart.html')

class CardAddView(View):
    
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id = product_id)
        form = CardAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')
        