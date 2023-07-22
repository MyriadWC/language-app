from django.urls import path
from .views import (
    DefinitionListView,
    DefinitionDetailView,
    DefinitionCreateView,
    DefinitionUpdateView,
    DefinitionDeleteView,
    UserDefinitionListView,
    LikeView
)
from . import views

urlpatterns = [
    path('', DefinitionListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserDefinitionListView.as_view(), name='user-definitions'),
    path('definition/<int:pk>/', DefinitionDetailView.as_view(), name='definition-detail'),
    path('definition/new/', DefinitionCreateView.as_view(), name='definition-create'),
    path('definition/<int:pk>/update/', DefinitionUpdateView.as_view(), name='definition-update'),
    path('definition/<int:pk>/delete/', DefinitionDeleteView.as_view(), name='definition-delete'),
    path('like/<int:pk>', LikeView, name='definition-like'),
    path('search/',views.search, name='search' ),
    path('about/', views.about, name='blog-about'),
]
