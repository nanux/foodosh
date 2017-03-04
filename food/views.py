from datetime import timedelta, date

from django.http import HttpResponse
from django.template import loader

from food.models import Side, Term, MealPlan


def index(request, year=2017, term=1, week=0):
    template = loader.get_template('food/index.html')

    term = Term.objects.get(year=year, term=term)
    if week == 0:
        week = Term.get_week(term, date.today())

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

    veggies = Side.objects.get(name='Veggies')
    late_tea = Side.objects.get(name='Late afternoon tea')
    context = {
        'term': term.term,
        'week': week,
        'meals': meals,
        'veggies': veggies,
        'late_tea': late_tea
    }
    return HttpResponse(template.render(context, request))
