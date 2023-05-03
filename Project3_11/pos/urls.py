from django.urls import path, include
from . import views
from .views import ValidateUserView
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

"""
This file defines the URL patterns for the project. Each URL pattern maps to a specific view function that handles
HTTP requests and produces an HTTP response. URL patterns can include variable components, allowing them to capture
values from the URL and pass them as arguments to the view function.

The URLs in this file include routes for authentication, validation, and various pages related to employee management
and reporting. The views for these URLs are defined in the `views.py` file in this directory.

Imported modules include:
- `path` from `django.urls`: used to define URL patterns
- `include` from `django.urls`: used to include URLs from other apps
- various views from `views.py`: used to map URLs to their corresponding views

Note: The `admin/doc` URL pattern is included for the purpose of generating Django admin documentation. It should not
be used in a production environment, as it can potentially expose sensitive information.
"""

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('validate_user/', ValidateUserView.as_view(), name='validate_user'),
    path('', views.login, name='login'),
    path('checkPermissions/', views.checkPermissions, name='checkPermissions'),
    path('/admin/doc/', include('django.contrib.admindocs.urls')),
    path('employee/', views.employee_page, name='employee'),
    path('order/', views.order_page, name='order'),
    path('reports/', views.reports_page, name='reports'),
    path('menuItems/', views.menuItems, name='menuItems'),
    path('database_info/', views.database_info, name='database_info'),
    path('button_testing/', views.button_testing, name='button_testing'),
    path('button_testing_page2/', views.button_testing_page2, name='button_testing_page2'),
    path('order_page/', views.order_page, name='order_page'),
    path('reports/', views.reports_page, name='reports'),
    path('salesReport/', views.salesReport, name='salesReport'),
    path('xReport/', views.xReport, name='xReport'),
    path('zReport/', views.zReport, name='zReport'),
    path('excessReport/', views.excessReport, name='excessReport'),
    path('restockReport/', views.restockReport, name='restockReport'),
    path('whatSalesTogetherReport/', views.whatSalesTogetherReport, name='whatSalesTogetherReport'),
    path('salesReportGeneration/', views.salesReportGeneration, name='salesReportGeneration'),
    path('xReportGeneration/', views.xReportGeneration, name='xReportGeneration'),
    path('zReportGeneration/', views.zReportGeneration, name='zReportGeneration'),
    path('excessReportGeneration/', views.excessReportGeneration, name='excessReportGeneration'),
    path('restockReportGeneration/', views.restockReportGeneration, name='restockReportGeneration'),
    path('whatSalesTogetherReportGeneration/', views.whatSalesTogetherReportGeneration, name='whatSalesTogetherReportGeneration'),
    path('editInventoryItems/', views.editInventoryItems, name='editInventoryItems'),
    path('editThisInventoryItem/', views.editThisInventoryItem, name='editThisInventoryItem'),
    path('submitInventoryEdit/', views.submitInventoryEdit, name='submitInventoryEdit'),
    path('edit_menu_items/', views.edit_menu_items, name='edit_menu_items'),
    path('edit_this_menu_item/', views.edit_this_menu_item, name='edit_this_menu_item'),
    path('submit_menu_edit/', views.submit_menu_edit, name='submit_menu_edit'),
    path('addInventoryItemPage/', views.addInventoryItemPage, name='addInventoryItemPage'),
    path('submitInventoryAddition/', views.submitInventoryAddition, name='submitInventoryAddition'),
    path('menuBoard/', views.menuBoard, name='menuBoard'),
]
