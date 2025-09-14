from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'price', 'stock_quality', 'status']
    list_filter = ['category', 'status']
    search_fields = ['sku', 'name']
    list_per_page = 10
    list_editable = ['status']
    list_display_links = ['sku', 'name']
    list_max_show_all = 100
    list_per_page = 100