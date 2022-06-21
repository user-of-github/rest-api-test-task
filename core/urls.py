from django.contrib import admin
from django.urls import path

from shop.views import ImportsAPIView
from shop.views import DeleteAPIView
from shop.views import NodesAPIView
from shop.views import SalesAPIView


urlpatterns = [
    path('admin', admin.site.urls),
    path('imports', ImportsAPIView.as_view()),
    path('delete/<str:to_delete>', DeleteAPIView.as_view()),
    path('nodes/<str:to_get>', NodesAPIView.as_view()),
    path('sales', SalesAPIView.as_view())
]
