# Django Product Ingestion System

A Django-based system for uploading, parsing, and managing product data from Excel/CSV files with a comprehensive admin interface and REST API.

## Features

- **File Upload**: Support for Excel (.xlsx, .xls) and CSV file uploads
- **Data Validation**: Column validation and data type checking
- **Duplicate Prevention**: Automatic handling of duplicate products based on SKU
- **Admin Interface**: Full-featured Django admin for product management
- **REST API**: Complete CRUD API with filtering, search, and pagination
- **API Documentation**: Interactive Swagger/ReDoc documentation

## Tech Stack

- **Backend**: Django 5.2.6
- **Database**: SQLite (default)
- **API Framework**: Django REST Framework
- **Data Processing**: Pandas, OpenPyXL
- **API Documentation**: drf-spectacular
- **Python**: 3.13+

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/zczqas/ProductSystem.git
cd ProductSystem
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Navigate to Project Directory

```bash
cd product_ingestion
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Start Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### Admin Interface

1. Access Django Admin at `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Navigate to "Products" to view and manage product data
4. Features available:
   - List view with filtering by category and status
   - Search by SKU, name, or category
   - Bulk editing of status and stock quantity
   - Detailed product editing with organized fieldsets

### File Upload API

#### Upload Products from File

**Endpoint**: `POST /api/products/upload_products/`

**Body**: 
- `file`: Excel (.xlsx, .xls) or CSV file

**Required File Columns**:
- `sku`: Stock Keeping Unit (must be unique)
- `name`: Product name
- `category`: Product category
- `price`: Product price (decimal)
- `stock_qty`: Stock quantity (integer)
- `status`: Product status ('active' or 'inactive')

**Example CSV Format**:
```csv
sku,name,category,price,stock_qty,status
PROD001,Wireless Headphones,Electronics,99.99,50,active
PROD002,Coffee Mug,Kitchen,15.50,100,active
PROD003,Notebook,Stationery,5.99,200,inactive
```

### REST API Endpoints

#### Authentication
For API access, you'll need to authenticate. The system supports both session and token authentication.

#### Product CRUD Operations

- **List Products**: `GET /api/products/`
- **Create Product**: `POST /api/products/`
- **Get Product**: `GET /api/products/{id}/`
- **Update Product**: `PUT /api/products/{id}/`
- **Partial Update**: `PATCH /api/products/{id}/`
- **Delete Product**: `DELETE /api/products/{id}/`
- **Upload Products**: `POST /api/products/upload_products/`

#### Filtering and Search

- Filter by category: `/api/products/?category=Electronics`
- Filter by status: `/api/products/?status=active`
- Search: `/api/products/?search=headphones`
- Ordering: `/api/products/?ordering=price`

### API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/`
- **Schema**: `http://127.0.0.1:8000/api/schema/`

## File Upload Process

1. **File Validation**: Checks file extension (.xlsx, .xls, .csv)
2. **Column Validation**: Ensures all required columns are present
3. **Data Processing**: Reads and processes each row
4. **Duplicate Handling**: Updates existing products or creates new ones based on SKU
5. **Error Reporting**: Provides detailed error messages for failed rows

## Error Handling

The system provides comprehensive error handling:

- **File Format Errors**: Invalid file types or corrupted files
- **Column Errors**: Missing required columns
- **Data Validation**: Invalid data types or values
- **Duplicate SKUs**: Automatic handling with update logic
- **Row-level Errors**: Detailed error reporting for specific rows

## Project Structure

```
product_ingestion/
├── manage.py
├── product_ingestion/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── products/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── tests.py
    └── migrations/
```

## Assumptions

1. **SKU Uniqueness**: SKUs are treated as unique identifiers
2. **File Format**: Excel and CSV files follow standard formats
3. **Status Values**: Only 'active' and 'inactive' are valid status values
4. **Price Validation**: Prices must be positive decimal values
5. **Stock Quantity**: Must be non-negative integers
6. **Data Updates**: Existing products are updated based on SKU matching

## Troubleshooting

### Common Issues

1. **Migration Errors**: Run `python manage.py makemigrations` then `python manage.py migrate`
2. **File Upload Errors**: Check file format and required columns
3. **Authentication Issues**: Ensure proper token or session authentication
4. **Permission Errors**: Check user permissions for file operations
