from django.urls import path, re_path
from . import views

urlpatterns = [
    path('list/', views.asset_list, name='list'),
    path("detail/<int:pk>/", views.asset_detail, name='asset_detail'),
    path('update/<int:pk>/', views.asset_update, name='asset_update'),
    path('delete/<int:pk>/', views.asset_delete, name='asset_delete'),
    path("assets_list", views.assetList_list, name = "assetList_list")
]