from django.urls import path

from menu import views


urlpatterns = [
    path('<path:item_slug>/', views.MenuView.as_view(), name='menu-item'),
    path('', views.MenuView.as_view(), name='menu-item-default'),
]
