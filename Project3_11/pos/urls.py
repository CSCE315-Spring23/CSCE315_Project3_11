from django.urls import path
from . import views
from .views import ValidateUserView

urlpatterns = [
    path('validate_user/', ValidateUserView.as_view(), name='validate_user'),
    path('', views.login, name='login'),
    path('employee/', views.employee_page, name='employee'),
    path('order/', views.order_page, name='order'),
    path('inventory/', views.inventory_page, name='inventory'),
    path('reports/', views.reports_page, name='reports'),
    path('menuItems/', views.menuItems, name='menuItems'),
    path('database_info/', views.database_info, name='database_info'),
    path('set-language/', views.set_language, name='set_language'),
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
]
