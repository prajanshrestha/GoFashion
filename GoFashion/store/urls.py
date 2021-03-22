from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from store.middlewares.auth import auth_middleware
from .views import home, signup, login, cart, orders, password_reset
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
    path('search', home.search, name='search'),
    path('profile', auth_middleware(profile), name='profile'),
    path('edit_profile/<int:id>', auth_middleware(edit_profile), name='edit_profile'),
    path('password_reset', password_reset.password_reset, name='password_reset'),
    path('reset_message', password_reset.reset_message, name='reset_message'),
]
