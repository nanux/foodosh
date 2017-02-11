import csv
from food.models import *

# Ingredients
# f = open('scripts/csv/ingredients.csv')
# csv = csv.reader(f, delimiter='\t')
#
# for line in csv:
#     print(line)
#
#     group = IngredientGroup.objects.get(name=line[0])
#     supplier = Supplier.objects.get(name=line[5])
#
#     # Ingredient.objects.get_or_create(name=line[1], group=group, supplier=supplier, package=line[2], brand=line[3], purpose=line[4], price=line[6])
#     ing = Ingredient.objects.get_or_create(name=line[1], group=group, supplier=supplier, package=line[2], brand=line[3], purpose=line[4],
#                price=line[6])
#
#     print(ing)

# Meals
f = open('scripts/csv/meals.csv')
csv = csv.reader(f, delimiter='\t')

for line in csv:
    print(line)

    group = MealGroup.objects.get(name=line[0])

    meal = Meal.objects.get_or_create(name=str(line[1]).capitalize(), group=group, description=line[2], ingredient_import=line[3])

    print(meal)
