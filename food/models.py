from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum


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
    def price_per_child(self):
        total = self.ingredients.all().aggregate(Sum('price'))
        if not total['price__sum']:
            total['price__sum'] = 0
        return '$' + str(round(total['price__sum'] / self.childCount, 3))

    @property
    def price_total(self):
        total = self.ingredients.all().aggregate(Sum('price'))
        if not total['price__sum']:
            total['price__sum'] = 0
        return '$' + str(round(total['price__sum'], 3))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class IngredientInMeal(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    count = models.IntegerField()
