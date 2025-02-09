from django.contrib import admin
from .models import User, Category, Product, Cart, CartItem, Order, OrderItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'created_at', 'updated_at')
    search_fields = ('session_id', 'user__username')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('product__name', 'cart__id')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'email', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'user__username')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
