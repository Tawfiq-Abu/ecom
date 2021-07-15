from django.contrib import admin
from .models import Category,Product
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # django fills the slug field with the name of the product
    prepopulated_fields = {'slug' : ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_by', 'slug', 'price', 'in_stock', 'uploaded']
    list_filter = ['in_stock','is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug' : ('name',)}
    