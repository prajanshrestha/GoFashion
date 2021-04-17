from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from store.models.product import Product


class ProductDescription(View):
    def get(self, request, ids):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        product = Product.objects.filter(id=ids)

        return render(request, 'product_description.html', {'product': product[0]})

    def post(self, request, ids):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart

        return HttpResponseRedirect(request.path_info)
