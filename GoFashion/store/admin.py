from django.contrib import admin

from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.product import Product
from .models.product_review_rating import ProductReviewRating


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'price', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'quantity', 'price', 'address', 'phone', 'date', 'order_completed']


class ProductReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'content', 'stars']


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductReviewRating, ProductReviewRatingAdmin)
