from __future__ import unicode_literals

import calendar

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class IngredientGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MealGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    package = models.CharField(max_length=100)
    group = models.ForeignKey(IngredientGroup, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    url = models.CharField(max_length=250, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    purpose = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.package)

    class Meta:
        ordering = ['name']


class Meal(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientInMeal', related_name='ingredients')
    childCount = models.IntegerField(default=130)
    description = models.CharField(max_length=255, blank=True)
    ingredient_import = models.CharField(max_length=255, blank=True)
    coeliac = models.CharField(max_length=250, blank=True)
    vegetarian = models.CharField(max_length=250, blank=True)
    vegan = models.CharField(max_length=250, blank=True)
    milk_intolerant = models.CharField(max_length=250, blank=True)
    group = models.ForeignKey(MealGroup, on_delete=models.CASCADE)

    @property
    def price_meal(self):
        total = 0
        for ing in self.ingredients.all():
            iim = IngredientInMeal.objects.get(ingredient=ing, meal=self)
            total += ing.price * iim.amount

        return round(total, 3)

    @property
    def price_total(self):
        # we sum veggies and late tea and the meal price
        veggies_price = 10
        try:
            veggies_price = Side.objects.get(name='Veggies').price
        except ObjectDoesNotExist:
            print("Using default value for veggies = {}", veggies_price)

        tea_price = 20
        try:
            tea_price = Side.objects.get(name='Late afternoon tea').price
        except ObjectDoesNotExist:
            print("Using default value for late afternoon tea = {}", tea_price)

        total = veggies_price + tea_price + self.price_meal
        return round(total, 3)

    @property
    def price_per_child(self):
        return round(self.price_total / self.childCount, 3)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Side(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.FloatField()
    description = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name


class IngredientInMeal(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    amount = models.IntegerField()


class MealPlan(models.Model):
    date = models.DateField()
    meals = models.ForeignKey(Meal, null=True)
    childCount = models.IntegerField(default=130)

    def __str__(self):
        return "{} - {}".format(self.date, calendar.day_name[self.date.weekday()])
