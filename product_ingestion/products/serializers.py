from rest_framework import serializers
from .models import Product, ProductStatusEnum


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model with validation and custom fields.
    """
    
    status_display = serializers.CharField(
        source='get_status_display', 
        read_only=True,
        help_text="Human-readable status display"
    )
    
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'category', 'price', 'stock_qty', 'status', 'status_display']
        read_only_fields = ['id']
        extra_kwargs = {
            'sku': {'help_text': 'Stock Keeping Unit - must be unique'},
            'name': {'help_text': 'Product name'},
            'category': {'help_text': 'Product category'},
            'price': {'help_text': 'Product price (must be greater than 0)'},
            'stock_qty': {'help_text': 'Stock quantity (must be non-negative)'},
            'status': {'help_text': 'Product status: active or inactive'},
        }
    
    def validate_sku(self, value):
        """Validate SKU uniqueness and format."""
        if not value:
            raise serializers.ValidationError("SKU cannot be empty.")
        
        # Check for uniqueness (excluding current instance for updates)
        instance = getattr(self, 'instance', None)
        if Product.objects.filter(sku=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("A product with this SKU already exists.")
        
        return value.upper()
    
    def validate_price(self, value):
        """Validate price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_stock_qty(self, value):
        """Validate stock quantity is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product lists."""
    
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'category', 'price', 'status']
