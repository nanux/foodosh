from datetime import timedelta, date

from django.http import HttpResponse
from django.template import loader

from food.models import Side, Term, MealPlan, IngredientInMeal


def index(request, year=2018, term=2, week=1):
    template = loader.get_template('food/index.html')

    term = Term.objects.get(year=year, term=term)
    if week == 0:
        week = Term.get_week(term, date.today())

    meals = get_meals(term, week)

    breakfast = Side.objects.get(name='Breakfast')
    veggies = Side.objects.get(name='Veggies')
    fruit = Side.objects.get(name='Fruit')
    for meal in meals:
        if meal is not None:
            meal.description = meal.description.split(",")
    context = {
        'term': term.term,
        'week': week,
        'meals': meals,
        'veggies': veggies,
        'fruit': fruit,
        'breakfast': breakfast
    }
    return HttpResponse(template.render(context, request))


def get_meals(term, week):
    start_date = term.start + timedelta(weeks=int(week) - 1)
    end_date = start_date + timedelta(weeks=1)
    plans = MealPlan.objects.filter(date__gte=start_date, date__lt=end_date)
    # if we don't have mealplan for a weekday we need to fill empty space
    meals = []
    for i in range(5):
        day = list(filter(lambda plan: plan.date.weekday() == i, plans))
        if len(day) > 0:
            meals.append(day[0].meal)
        else:
            meals.append(None)
    return meals


def ingredients_weeks(request):
    template = loader.get_template('food/shopping_list.html')
    return HttpResponse(template.render(request))


def shopping_list(request, year, term, week):
    template = loader.get_template('food/shopping_list.html')

    term = Term.objects.get(year=year, term=term)

    meals = get_meals(term, week)
    ingredients = {}

    for meal in meals:
        for ingredient in meal.ingredients.all():
            iim = IngredientInMeal.objects.get(meal=meal, ingredient=ingredient)
            ingredient_name = iim.ingredient.name.strip()
            if ingredient_name in ingredients:
                ingredients[ingredient_name] += iim.amount
            else:
                ingredients[ingredient_name] = iim.amount

    context = {
        'term': term.term,
        'week': week,
        'meals': meals,
        'ingredients': ingredients,
    }
    return HttpResponse(template.render(context, request))
