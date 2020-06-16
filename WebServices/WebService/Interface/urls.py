from django.urls import path

from . import views
from .views import (
	PostListView, 
	PostDetailView, 
	PostCreateView,
	PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    path('', views.home, name='UI-home'),
    path('service/', views.service, name='UI-service'),
    path('service/checkTVA/', PostListView.as_view(), name='TVA'),
    path('file/<int:pk>/', PostDetailView.as_view(), name='file-detail'),
    path('file/new/', PostCreateView.as_view(), name='file-upload'),
    path('file/<int:pk>/update/', PostUpdateView.as_view(), name='file-update'),
    path('file/<int:pk>/delete/', PostDeleteView.as_view(), name='file-delete'),
    path('about/', views.about, name='UI-about'),
    path('file/execution/', views.execute, name='file-execute'),
    path('file/visualization/', views.visualization, name='file-visualization'),
]