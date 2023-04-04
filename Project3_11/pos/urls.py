from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('employee/', views.employee_page, name='employee'),
    path('database_info/', views.database_info, name='database_info'),
]
