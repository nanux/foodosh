from __future__ import unicode_literals

from django.db import models


class IngredientGroup(models.Model):
    name = models.CharField(max_length=100)


class MealGroup(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
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


class Meal(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientInMeal')
    childCount = models.IntegerField(default=130)
    description = models.CharField(max_length=255, blank=True)
    coeliac = models.CharField(max_length=250, blank=True)
    vegetarian = models.CharField(max_length=250, blank=True)
    vegan = models.CharField(max_length=250, blank=True)
    milk_intolerant = models.CharField(max_length=250, blank=True)
    group = models.ForeignKey(MealGroup, on_delete=models.CASCADE)


class IngredientInMeal(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    count = models.IntegerField()
