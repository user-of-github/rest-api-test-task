from django.contrib import admin
from django.urls import path
from shop.views import ImportsAPIView
from shop.views import DeleteAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('imports/', ImportsAPIView.as_view()),
    path('delete/<str:to_delete>/', DeleteAPIView.as_view())
]
