# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

# app_name = 'inventory'

urlpatterns = [
    
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
      # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),

    # Clock Types
    path('clocktypes/', views.ClockTypeListView.as_view(), name='clocktype_list'),
    path('clocktypes/add/', views.ClockTypeCreateView.as_view(), name='clocktype_create'),
    
    # Stock
    path('stocks/', views.StockListView.as_view(), name='stock_list'),
    path('stocks/add/', views.StockCreateView.as_view(), name='stock_create'),
    
    # Sales
    path('sales/', views.SaleListView.as_view(), name='sale_list'),
    path('sales/add/', views.SaleCreateView.as_view(), name='sale_create'),
    
    # Returns
    path('returns/', views.ReturnListView.as_view(), name='return_list'),
    path('returns/add/', views.ReturnCreateView.as_view(), name='return_create'),
    
    # Summary
    path('summary/', views.inventory_summary, name='summary'),
]