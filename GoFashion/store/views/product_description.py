from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from store.models.product import Product
from store.views.product_review_rating import recommendation


class ProductDescription(View):
    def get(self, request, ids):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        product = Product.objects.filter(id=ids)
        print(product)

        for item in product:
            # recommendation of product
            recommended = recommendation(item.name, request.session.get('customer'), item.id)
            product_object_list = []
            if recommended is not None:

                for items in range(len(recommended)):
                    item = Product.objects.get(name=recommended[items])
                    product_object_list.append(item)
            print(product_object_list)
            data = {
                'product': product[0],
                'recommend': product_object_list
            }
        return render(request, 'product_description.html', data)

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
