from django.contrib import admin
from .models import StorehouseRecord, StatusHistory


@admin.register(StorehouseRecord)
class StorehouseRecordAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'receiver_name', 'places_count', 'status', 'amount_paid', 'cashless_payment', 'date', 'created_by', 'updated_by', 'updated_at')
    list_filter = ('status', 'cashless_payment', 'date')
    search_fields = ('sender_name', 'receiver_name', 'sender_phone', 'receiver_phone')
    readonly_fields = ('created_by', 'updated_by', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('storehouse_record', 'old_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('old_status', 'new_status', 'changed_at')
    search_fields = ('storehouse_record__sender_name', 'storehouse_record__receiver_name', 'changed_by__username')
    readonly_fields = ('storehouse_record', 'old_status', 'new_status', 'changed_by', 'changed_at')
