from django.shortcuts import redirect
from django.views import View

from store.models import Customer
from store.models.orders import Order
from store.models.product import Product


class Checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')  # cart contains quantity of products
        products = Product.get_products_by_id(list(cart.keys()))

        for product in products:
            order = Order(
                customer=Customer(id=customer),
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=cart.get(str(product.id))
            )
            order.save()
        request.session['cart'] = {}

        return redirect('orders')
