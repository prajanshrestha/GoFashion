from django.urls import path

from store.middlewares.auth import auth_middleware
from .views import home, signup, login, cart, orders
from .views.checkout import Checkout
from .views.login import logout

urlpatterns = [
    path('', home.Index.as_view(), name='index'),
    path('signup', signup.Signup.as_view(), name='signup'),
    path('login', login.Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', cart.Cart.as_view(), name='cart'),
    path('checkout', Checkout.as_view(), name='checkout'),
    path('orders', auth_middleware(orders.OrderView.as_view()), name='orders'),
]
