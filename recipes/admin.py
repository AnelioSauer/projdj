from django.contrib import admin

from .models import Category
from .models import Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...

# Modo 1 para registrar uma classe, neste caso o recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


# Modo 2 para registrar uma classe, neste caso o category
admin.site.register(Category, CategoryAdmin)
