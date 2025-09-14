from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pandas as pd
import os
from datetime import datetime

from .models import Product, ProductStatusEnum
from .serializers import ProductSerializer, ProductListSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all products",
        description="Retrieve a paginated list of all products with optional filtering and search.",
        tags=["Products"],
    ),
    create=extend_schema(
        summary="Create a new product",
        description="Create a new product with the provided data.",
        tags=["Products"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a product",
        description="Get detailed information about a specific product.",
        tags=["Products"]
    ),
    update=extend_schema(
        summary="Update a product",
        description="Update all fields of a specific product.",
        tags=["Products"]
    ),
    partial_update=extend_schema(
        summary="Partially update a product",
        description="Update specific fields of a product.",
        tags=["Products"]
    ),
    destroy=extend_schema(
        summary="Delete a product",
        description="Delete a specific product.",
        tags=["Products"]
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products with full CRUD operations.
    """
    
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'status']
    ordering = ['sku']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    @extend_schema(
        summary="Upload products from file",
        description="Upload products from Excel (.xlsx) or CSV file. The file should contain columns: sku, name, category, price, stock_qty, status",
        tags=["Products"],
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'Excel (.xlsx) or CSV file containing product data'
                    }
                },
                'required': ['file']
            }
        }
    )
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_products(self, request):
        """Upload products from Excel or CSV file."""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # Validate file type
        allowed_extensions = ['.xlsx', '.xls', '.csv']
        file_extension = os.path.splitext(file.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            return Response(
                {'error': f'File type not supported. Allowed types: {", ".join(allowed_extensions)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_filename = f"temp_upload_{timestamp}_{file.name}"
            temp_path = default_storage.save(temp_filename, ContentFile(file.read()))
            
            if file_extension == '.csv':
                df = pd.read_csv(default_storage.path(temp_path))
            else:
                df = pd.read_excel(default_storage.path(temp_path))
            
            default_storage.delete(temp_path)
            
            required_columns = ['sku', 'name', 'category', 'price', 'stock_qty', 'status']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing required columns: {", ".join(missing_columns)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            created_count = 0
            updated_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    sku = str(row['sku']).strip().upper()
                    name = str(row['name']).strip()
                    category = str(row['category']).strip()
                    price = float(row['price'])
                    stock_qty = int(row['stock_qty'])
                    status_value = str(row['status']).strip().lower()
                    
                    if status_value not in ['active', 'inactive']:
                        status_value = 'inactive'  # Default to inactive
                    
                    product, created = Product.objects.get_or_create(
                        sku=sku,
                        defaults={
                            'name': name,
                            'category': category,
                            'price': price,
                            'stock_qty': stock_qty,
                            'status': status_value
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        product.name = name
                        product.category = category
                        product.price = price
                        product.stock_qty = stock_qty
                        product.status = status_value
                        product.save()
                        updated_count += 1
                        
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")  # +2 because pandas is 0-indexed and we skip header
            
            response_data = {
                'message': 'File processed successfully',
                'created': created_count,
                'updated': updated_count,
                'total_processed': created_count + updated_count
            }
            
            if errors:
                response_data['errors'] = errors[:10]  # Limit to first 10 errors
                if len(errors) > 10:
                    response_data['error_count'] = len(errors)
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error processing file: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )