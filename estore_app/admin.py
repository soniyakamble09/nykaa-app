from django.contrib import admin
from .models import Product, Categories

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','cat','is_active']
    list_filter=['cat','is_active']

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'cat']  
    search_fields = ['cat']

admin.site.register(Product, ProductAdmin)
admin.site.register(Categories, CategoriesAdmin)