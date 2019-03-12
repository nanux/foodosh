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


class TermTestCase(TestCase):

    def test_end_date_autofill(self):
        term1 = Term.objects.create(term=1, year=2019, weeks=1, start=datetime.date(2019, 1, 1))
        self.assertEqual(term1.end, datetime.date(2019, 1, 8))

    def test_get_term_when_date_in_term(self):
        first_date = datetime.date(2019, 1, 1)
        term_expected = Term.objects.create(term=1, year=2019, weeks=1, start=datetime.date(2019, 1, 1))
        term_actual = Term.get_term_from_date(first_date)

        self.assertEqual(term_expected, term_actual)

    def test_get_term_when_date_between_terms(self):
        term_first = Term.objects.create(term=1, year=2019, weeks=1, start=datetime.date(2019, 1, 1))
        term_second = Term.objects.create(term=1, year=2021, weeks=1, start=datetime.date(2021, 1, 1))
        date_between = datetime.date(2020, 1, 1)

        actual_term = Term.get_term_from_date(date_between)
        self.assertEqual(actual_term, term_second)

    def test_get_term_when_no_future_or_current_term(self):
        term_in_past = Term.objects.create(term=1, year=2019, weeks=1, start=datetime.date(2019, 1, 1))
        term_in_past_past = Term.objects.create(term=1, year=2018, weeks=1, start=datetime.date(2018, 1, 1))
        date_now = datetime.date(2020, 1, 1)

        actual_term = Term.get_term_from_date(date_now)
        self.assertEqual(actual_term, term_in_past)
