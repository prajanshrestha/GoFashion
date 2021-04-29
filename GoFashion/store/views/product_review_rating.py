from django.http import HttpResponseRedirect

from store.models import Customer
from store.models.product import Product
from store.models.product_review_rating import ProductReviewRating


def product_review_rating(request, ids):
    product = Product.objects.get(id=ids)
    if request.method == 'POST':
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')
        customer_id = request.session.get('customer')
        user = Customer.objects.get(id=customer_id)

        review = ProductReviewRating.objects.create(product=product,
                                                    customer=user,
                                                    stars=stars,
                                                    content=content)

    url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(url)
