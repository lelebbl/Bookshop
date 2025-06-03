from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('sales-by-month/', views.sales_by_month, name='sales_by_month'),
    path('customer-analytics/', views.customer_analytics, name='customer_analytics'),
    path('products/demand/', views.product_demand_analytics, name='product_demand'),
    path('analytics/category/', views.category_analytics, name='category_analytics'),
]
