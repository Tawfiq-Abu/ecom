from django.contrib import admin
from .models import Receipt, QrCode

# Register your models here.
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['product_name','item_qty','total_price','code']

admin.site.register(QrCode)