from django.http import HttpResponse
from django.template import loader

from food.models import Meal, Side


def index(request):
    template = loader.get_template('food/index.html')
    # this needs to be replaced by dynamic fetch from the meal plan
    # don't look at me, I am sick and I need to get this done before lunch :)
    meals = []
    meals.append(Meal.objects.get(id=6))
    meals.append(Meal.objects.get(id=12))
    meals.append(Meal.objects.get(id=22))
    meals.append(Meal.objects.get(id=32))
    meals.append(Meal.objects.get(id=11))
    veggies = Side.objects.get(name='Veggies')
    late_tea = Side.objects.get(name='Late afternoon tea')
    context = {
        'meals': meals,
        'veggies': veggies,
        'late_tea': late_tea
    }
    return HttpResponse(template.render(context, request))
