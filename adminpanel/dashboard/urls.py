from django.urls import path
from . import views

urlpatterns = [
    path('sales-chart/', views.sales_chart, name='sales_chart'),
]
