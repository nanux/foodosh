from django.http import HttpResponse
from django.template import loader

from food.models import Meal, Side


def index(request):
    meals = Meal.objects.all()
    template = loader.get_template('food/index.html')
    meals = meals.filter(id__in=[1,2,3,4,5])
    veggies = Side.objects.get(name='Veggies')
    late_tea = Side.objects.get(name='Late afternoon tea')
    context = {
        'meals': meals,
        'veggies': veggies,
        'late_tea': late_tea
    }
    return HttpResponse(template.render(context, request))
