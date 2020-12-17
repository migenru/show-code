from django.contrib import admin

from .models import Category, Product, AttributeValue, ProductAttribute, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'parent')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'price', 'categoty', 'quentity')


admin.site.register(ProductAttribute)
admin.site.register(ProductImage)
admin.site.register(AttributeValue)
