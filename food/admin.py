from django.contrib import admin
from django.forms import TextInput, Textarea

from .models import *

class IngredientInline(admin.TabularInline):
    model = IngredientInMeal
    extra = 1

class MealAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'show_ingredients', 'price_per_child', 'price_total']
    inlines = (IngredientInline,)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'120'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


    def show_ingredients(self, obj):
        return "\n".join([a.name for a in obj.ingredients.all()])


admin.site.register(Ingredient)
admin.site.register(IngredientGroup)
admin.site.register(Meal, MealAdmin)
admin.site.register(MealGroup)
admin.site.register(Supplier)
admin.site.register(IngredientInMeal)


