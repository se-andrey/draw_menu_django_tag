from django.urls import path

from menus.views import MenuView

urlpatterns = [
    path('<str:url>/', MenuView.as_view(), name='menu_view'),
]
