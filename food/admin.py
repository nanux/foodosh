from django.contrib import admin
from .models import Ingredient, IngredientGroup, Meal, MealGroup, Supplier, IngredientInMeal

# Register your models here.

admin.site.register(Ingredient)
admin.site.register(IngredientGroup)
admin.site.register(Meal)
admin.site.register(MealGroup)
admin.site.register(Supplier)
admin.site.register(IngredientInMeal)
