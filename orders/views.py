from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CardAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
import requests
from django.conf import settings
import json
from django.http import HttpResponse


class CartView(View):

    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart':cart})

class CardAddView(View):
    
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id = product_id)
        form = CardAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')
        


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id = product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id = order_id)
        return render(request, 'orders/order.html', {'order':order})


class OrderCreateView(LoginRequiredMixin, View):
    
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user = request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

\

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/orders/verify/'
Amount = Order.get_total_price
class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        Phone = request.user.phone_number
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": Amount,
            "Description": description,
            "Phone": Phone,
            "CallbackURL": CallbackURL,
        }
        header = {"accept": "application/json", "content-type": "application/json'"}

        data = requests.post(url=ZP_API_REQUEST, data=json.dumps(data), headers=header)
            
        authority = data.json()['data']['authority']
        if len(data.json()['errors']) == 0:
                return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
                e_code = data.json()['errors']['code']
                e_message = data.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")