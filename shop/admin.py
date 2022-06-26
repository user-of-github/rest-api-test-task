from django.contrib import admin
from .models import ShopUnit, HistoryTable, ShopUnitHistory


class ShopUnitAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name', 'date', 'type', 'price', 'parentId', 'children', 'totally_inner_goods_count', 'total_inner_sum')


class ShopUnitHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name', 'date', 'type', 'price', 'parentId')


class HistoryTableAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'history_objects')


admin.site.register(ShopUnit, ShopUnitAdmin)
admin.site.register(HistoryTable, HistoryTableAdmin)
admin.site.register(ShopUnitHistory, ShopUnitHistoryAdmin)
