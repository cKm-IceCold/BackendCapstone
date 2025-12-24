from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Property
    path('', views.PropertyListView.as_view(), name='property_list'),
    path('property/add/', views.PropertyCreateView.as_view(), name='property_add'),
    path('property/<int:pk>/edit/', views.PropertyUpdateView.as_view(), name='property_edit'),
    path('property/<int:pk>/delete/', views.PropertyDeleteView.as_view(), name='property_delete'),
]
