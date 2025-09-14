from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'price', 'stock_qty', 'status']
    list_filter = ['category', 'status']
    search_fields = ['sku', 'name', 'category']
    list_per_page = 25
    list_editable = ['status', 'stock_qty']
    list_display_links = ['sku', 'name']
    list_max_show_all = 100
    ordering = ['sku']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('sku', 'name', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock_qty')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )