# quotations/urls.py
from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),  # Remove the duplicate home path
    path('request-quote/', views.request_quote, name='request_quote'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Changed from 'admin/' to avoid conflict with Django admin
    path('update-status/<int:project_id>/', views.update_project_status, name='update_project_status'),
    path('project/<int:project_id>/', views.project_details, name='project_details'),
    path('materials/', views.materials_list, name='materials_list'),
    path('create-material/', views.create_material, name='create_material'),
    path('update-material/<int:material_id>/', views.update_material, name='update_material'),
    path('delete-material/<int:material_id>/', views.delete_material, name='delete_material'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]