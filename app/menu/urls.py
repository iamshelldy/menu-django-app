from django.urls import path

from menu import views


urlpatterns = [
    path('', views.MenuView.as_view(), name='menu-item-default'),
    path('<path:item_slug>/', views.MenuView.as_view(), name='menu-item'),
]
