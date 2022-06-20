from django.contrib import admin
from .models import ShopUnit


class ShopUnitAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name', 'date', 'type', 'price', 'parentId', 'children', 'totally_inner_goods_count', 'total_inner_sum')


admin.site.register(ShopUnit, ShopUnitAdmin)
