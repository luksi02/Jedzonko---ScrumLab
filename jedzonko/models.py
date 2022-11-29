from django.db import models

WEEK_DAYS = (
    (0, "Poniedziałek"),
    (1, "Wtorek"),
    (2, "Środa"),
    (3, "Czwartek"),
    (4, "Piątek"),
    (5, "Sobota"),
    (6, "Niedziela"),
)


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    ingredients = models.CharField(max_length=512)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField()
    preparation_method = models.TextField(default="")
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, related_name="plans", through="RecipePlan")

    def __str__(self):
        return self.name


class DayName(models.Model):
    day = models.SmallIntegerField(choices=WEEK_DAYS, default=0)


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.SmallIntegerField(null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    day = models.ForeignKey(DayName, on_delete=models.CASCADE)

    def __str__(self):
        return self.meal_name


class Page(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(default="")
    slug = models.SlugField(max_length=128)