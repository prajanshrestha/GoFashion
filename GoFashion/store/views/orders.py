from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View

from store.models.orders import Order


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)

        # pagination
        paginator = Paginator(orders, 3)
        page = request.GET.get('page')
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        data = {
            'orders': orders,
            'page': page
        }

        return render(request, 'orders.html', data)
