from __future__ import unicode_literals

from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.safestring import mark_safe


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
    group = models.ForeignKey(MealGroup, on_delete=models.CASCADE)
    childCount = models.IntegerField(default=130)
    description = models.CharField(max_length=255, blank=True)
    ingredient_import = models.CharField(max_length=255, blank=True)
    coeliac = models.CharField(max_length=250, blank=True)
    vegetarian = models.CharField(max_length=250, blank=True)
    vegan = models.CharField(max_length=250, blank=True)
    milk_intolerant = models.CharField(max_length=250, blank=True)
    url = models.URLField(blank=True)
    picture_url = models.URLField(blank=True)

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
        try:
            veggies_price = Side.objects.get(name='Veggies').price
        except ObjectDoesNotExist:
            print("Using default value for veggies = {}", veggies_price)

        try:
            fruit_price = Side.objects.get(name='Fruit').price
        except ObjectDoesNotExist:
            print("Using default value for fruit = {}", fruit_price)

        total = veggies_price + fruit_price + self.price_meal
        return round(total, 3)

    @property
    def price_per_child(self):
        return round(self.price_total / self.childCount, 3)

    def image_tag(self):
        return mark_safe('<a href="%s" target="_blank"><img src="%s" width="150" /></a>' % (self.url, self.picture_url))

    image_tag.short_description = 'Image'

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
    meal = models.ForeignKey(Meal, null=True)
    childCount = models.IntegerField(default=130)

    def __str__(self):
        date = self.date.strftime('%d/%m/%y (%a)')
        return "{} - {}".format(date, self.meal.name)

    @property
    def get_term(self):
        return Term.get_term_from_date(self.date)

    @property
    def get_week_and_term(self):
        term = self.get_term
        week = term.get_week(term, self.date)
        return "{}/{} - W{}".format(term.year, term.term, week)

    class Meta:
        ordering = ['date']


class Term(models.Model):
    term = models.IntegerField()
    year = models.IntegerField()
    weeks = models.IntegerField(default=10)
    start = models.DateField()
    end = models.DateField(blank=True, help_text="Don't fill")

    def save(self, *args, **kwargs):
        if not self.end:
            self.end = self.start + timedelta(weeks=self.weeks)
        super(Term, self).save(*args, **kwargs)

    def __str__(self):
        return "{}/{} ({} - {})".format(self.year, self.term, self.start.strftime("%d/%m"), self.end.strftime("%d/%m"))

    @classmethod
    def get_term_from_date(cls, date):
        return Term.objects.get(start__lte=date, end__gte=date)

    @staticmethod
    def get_week(term, date):
        monday1 = (term.start - timedelta(days=term.start.weekday()))
        monday2 = (date - timedelta(days=date.weekday()))
        return int((monday2 - monday1).days / 7) + 1
