from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from store.middlewares.auth import auth_middleware
from .views import home, signup, login, cart, orders
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
    path('profile', profile, name='profile'),
    path('search', home.search, name='search'),
    path('edit-profile', edit_profile, name='edit_profile'),
]
