from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('employee/', views.employee_page, name='employee'),
]
