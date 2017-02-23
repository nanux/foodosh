from django.http import HttpResponse
from django.template import loader

from food.models import Meal


def index(request):
    meals = Meal.objects.all()
    template = loader.get_template('food/index.html')
    meals = meals.filter(id__in=[1,2,3,4,5])
    context = {
        'meals': meals,
    }
    return HttpResponse(template.render(context, request))
