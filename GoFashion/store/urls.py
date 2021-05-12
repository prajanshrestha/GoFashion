from django.urls import path
from store.middlewares.auth import auth_middleware
from .views import home, signup, login, cart, orders, product_description, product_review_rating, online_payment
from .views.checkout import Checkout
from .views.login import logout, profile, edit_profile

urlpatterns = [
    path('', home.Index.as_view(), name='index'),
    path('signup', signup.Signup.as_view(), name='signup'),
    path('login', login.Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', cart.Cart.as_view(), name='cart'),
    path('checkout', Checkout.as_view(), name='checkout'),
    path('orders', auth_middleware(orders.OrderView.as_view()), name='orders'),
    path('search', home.Search.as_view(), name='search'),
    path('profile/<int:id>', auth_middleware(profile), name='profile'),
    path('edit_profile/<int:id>', auth_middleware(edit_profile), name='edit_profile'),
    path('product_description/<int:ids>', product_description.ProductDescription.as_view(), name='product_description'),
    path('product_review_rating/<int:ids>', product_review_rating.product_review_rating, name='product_review_rating'),
    # path('online_payment/<int:pk>/', online_payment.online_payment, name='online_payment'),
    # path('payment_complete', online_payment.payment_complete, name='payment_complete'),
]
