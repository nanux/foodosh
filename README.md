# Foodosh

## Planning meals with ease

Foodosh is a very simple application which helps with meals planning
(e.g. in canteen or after care). It also provides shopping lists and
produce accessible menu which can be displayed on a page.

## Requirements

The application is written in Python 3 using Django framework. You need
to install `Python 3` and `pip` package manager. Then you can install
additional dependencies.

    pip install -r requirements.txt

## Development

First migrate and then run server via:

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Then you can head to `http://localhost:8000`:
All changes are reflected dynamically.

## Deployment

The app can be deployed to Heroku on Google App Engine.

## Usage

Menu is displayed on the index page:
http://localhost:8000

Admin is available on (you can log with a superuser created previously):
http://localhost:8000/admin/

- `Meals` are composed from `Ingredients`
- The year can be sliced into separate `Terms` which are defined via
`Start date` and number of `weeks`
- `MealPlan` defines a date from a `Term` and assigns `Meal` for the
 particular day. This day is then reflected on the main menu.


----
Bon Appetit