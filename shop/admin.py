from django.contrib import admin
from .models import ShopUnit


class ShopUnitAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name', 'date', 'type', 'price', 'parentId', 'children')


admin.site.register(ShopUnit, ShopUnitAdmin)
