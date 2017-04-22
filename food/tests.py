import datetime

from django.test import TestCase

from food.models import MealPlan, Meal, MealGroup, Term
from food.views import get_meals


class MealPlanTestCase(TestCase):
    def test_meals_displayed_in_a_week_not_starting_on_monday(self):
        group = MealGroup.objects.create(name='group')
        meal_wed = Meal.objects.create(name="Wednesday meal", group=group)
        meal_mon = Meal.objects.create(name="Monday meal", group=group)

        wednesday = MealPlan.objects.create(date=datetime.date(2017, 4, 26), meal=meal_wed)
        monday = MealPlan.objects.create(date=datetime.date(2017, 5, 1), meal=meal_mon)

        self.assertEqual(Meal.objects.count(), 2)
        self.assertEqual(MealPlan.objects.count(), 2)

        term = Term.objects.create(term=1, year=2017, start=datetime.date(2017, 4, 24))

        meals = get_meals(term, 1)
        self.assertEqual(len(list(filter(lambda meal: meal != None, meals))), 1)
        self.assertIn(meal_wed, meals)
        self.assertNotIn(meal_mon, meals)
