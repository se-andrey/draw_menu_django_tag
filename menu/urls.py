from django.contrib import admin
from django.urls import include, path

from menus.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', include(('menus.urls', 'menus'), namespace='menus')),
    path('', IndexView.as_view(), name='index'),

]
