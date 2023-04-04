from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('employee/', views.employee_page, name='employee'),
    path('order/', views.order_page, name='order'),
    path('menuItems/', views.menuItems, name='employee'),
    path('database_info/', views.database_info, name='database_info'),
]
