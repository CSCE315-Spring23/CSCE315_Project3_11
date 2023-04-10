from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('employee/', views.employee_page, name='employee'),
    path('order/', views.order_page, name='order'),
    path('inventory/', views.inventory_page, name='inventory'),
    path('reports/', views.reports_page, name='reports'),
    path('menuItems/', views.menuItems, name='employee'),
    path('database_info/', views.database_info, name='database_info'),
]
