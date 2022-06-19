from django.contrib import admin
from django.urls import path
from shop.views import ImportsAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('imports/', ImportsAPIView.as_view())
]
