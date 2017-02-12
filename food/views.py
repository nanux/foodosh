from django.http import HttpResponse
from django.template import loader

from food.models import Meal


def index(request):
    meals = Meal.objects.all()
    template = loader.get_template('food/index.html')
    context = {
        'meals': meals,
        'mon_meal': meals.get(id=1),
        'tue_meal': meals.get(id=2),
        'wed_meal': meals.get(id=3),
        'thu_meal': meals.get(id=4),
        'fri_meal': meals.get(id=5),
    }
    return HttpResponse(template.render(context, request))
