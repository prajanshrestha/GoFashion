from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from store.models.category import Category
from store.models.product import Product


class Index(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_category_id(categoryID)
        else:
            products = Product.get_all_products()

        # print('You are:', request.session.get('email'))

        # pagination
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        data = {
            'products': products,
            'categories': categories,
            'page': page
        }

        return render(request, 'index.html', data)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        url = request.POST.get('url')
        print(url)
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
        if url is not None:
            return redirect(url)
        return redirect('index')


class Search(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = "products"
    paginate_by = 1

    def get_queryset(self):
        request = self.request
        query = request.GET.get('search', None)

        if query is not None:
            lookup = Q(name__icontains=query) | Q(description__icontains=query)
            return Product.objects.filter(lookup).distinct()
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        request = self.request
        query = request.GET.get('search', None)
        context['query_value'] = query
        return context
