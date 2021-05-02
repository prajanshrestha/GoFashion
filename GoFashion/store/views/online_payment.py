# import json
#
# from django.http import JsonResponse
# from django.shortcuts import render
#
# from store.models import Product, Order
#
#
# def online_payment(request, pk):
#     products = Product.objects.get(id=pk)
#     context = {'products': products}
#     return render(request, 'online_payment.html', context)
#
#
# def payment_complete(request):
#     body = json.loads(request.body)
#     print('BODY:', body)
#     products = Product.objects.get(id=body['productId'])
#     Order.objects.create(
#         products=products
#     )
#
#     return JsonResponse(request, 'Payment completed!', safe=False)
