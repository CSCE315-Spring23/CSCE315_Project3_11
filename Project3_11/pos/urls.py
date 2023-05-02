from django.urls import path, include
from . import views
from .views import ValidateUserView
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', TemplateView.as_view(template_name="oAuth.html")),
    path('accounts/', include('allauth.urls')),
    # path('logout', LogoutView.as_view()),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('validate_user/', ValidateUserView.as_view(), name='validate_user'),
    path('', views.login, name='login'),
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
