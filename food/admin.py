from django.contrib import admin
from django.forms import TextInput, Textarea

from .models import *


class IngredientInline(admin.TabularInline):
    model = IngredientInMeal
    extra = 1


class MealAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image_tag', 'show_ingredients', 'price_meal', 'price_total', 'price_per_child']
    inlines = (IngredientInline,)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '120'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    # fields = ('image_tag',)
    readonly_fields = ('image_tag',)

    def show_ingredients(self, obj):
        return "\n".join([a.name for a in obj.ingredients.all()])


class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['_date', 'meal', 'get_week_and_term']

    def _date(self, obj):
        return obj.date.strftime('%d/%m/%y (%a)')


admin.site.register(Ingredient)
admin.site.register(Meal, MealAdmin)
admin.site.register(MealGroup)
admin.site.register(Supplier)
admin.site.register(MealPlan, MealPlanAdmin)
admin.site.register(Side)
admin.site.register(Term)
