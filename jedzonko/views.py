from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from .models import Recipe, Plan, RecipePlan, DayName, Page
from random import shuffle
from django.core.paginator import Paginator


class IndexHtmlView(View):
    def get(self, request):
        recipes = list(Recipe.objects.all())
        shuffle(recipes)

        if Page.objects.filter(slug="contact").exists():
            contact_link = "contact"
        else:
            contact_link = "#contact"

        if Page.objects.filter(slug="about_app").exists():
            about_app_link = "about_app"
        else:
            about_app_link = "#about"

        ctx = {
            "recipes_for_carousel": recipes[0:3],
            "contact_link": contact_link,
            "about_app_link": about_app_link
        }
        return render(request, "index.html", ctx)


class DashboardView(View):
    def get(self, request):
        number_of_plans = Plan.objects.count()
        number_of_recipes = Recipe.objects.count()
        latest_plan = Plan.objects.all().order_by('-created')[0]
        day_ids = RecipePlan.objects.filter(plan_id=latest_plan.id).values_list("day_id")
        recipe_plans = RecipePlan.objects.all().filter(plan_id=latest_plan).order_by("order")

        days = set()
        for day in day_ids:
            days.add(DayName.objects.get(pk=day[0]))

        ctx = {
            "number_of_plans": number_of_plans,
            "number_of_recipes": number_of_recipes,
            "latest_plan": latest_plan,
            "days": days,
            "recipe_plans": recipe_plans,
        }

        return render(request, "dashboard.html", ctx)


class RecipeIdView(View):
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        return render(request, "app-recipe-details.html", {"recipe": recipe})

    def post(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        if request.POST.get('like'):
            recipe.votes += 1
        else:
            recipe.votes -= 1
        recipe.save()
        return redirect('recipe-id', id=recipe.id)


class RecipeAdd(View):
    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        name = request.POST.get("name")
        ingredients = request.POST.get("ingredients")
        description = request.POST.get("description")
        preparation_time = request.POST.get("preparation_time")
        preparation_method = request.POST.get("preparation_method")

        if not name or not ingredients or not description or not preparation_time or not preparation_method:
            return render(request, "app-add-recipe.html", {"error": "Wypełnij poprawnie wszystkie pola"})

        Recipe.objects.create(name=name, ingredients=ingredients, description=description,
                              preparation_time=preparation_time, preparation_method=preparation_method)

        return redirect(reverse('recipes-list'))


class RecipeModify(View):
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)

        if request.session.get("error"):
            request.session["error"] = False
            return render(request, "app-edit-recipe.html", {"recipe": recipe,
                                                            "error": "Wypełnij poprawnie wszystkie pola"})
        return render(request, "app-edit-recipe.html", {"recipe": recipe})

    def post(self, request, id):
        name = request.POST.get("name")
        description = request.POST.get("description")
        prep_time = int(request.POST.get("prep-time"))
        prep_method = request.POST.get("prep-method")
        ingredients = request.POST.get("ingredients")

        if name and description and prep_time and prep_method and ingredients:
            Recipe.objects.create(name=name, ingredients=ingredients, description=description,
                                  preparation_time=prep_time, preparation_method=prep_method)
            return redirect('recipes-list')

        request.session["error"] = True
        return redirect('recipe-modify', id=id)


class PlanIdView(View):
    def get(self, request, id):
        plan = get_object_or_404(Plan, id=id)
        day_ids = RecipePlan.objects.filter(plan_id=plan.id).values_list("day_id")
        recipe_plans = RecipePlan.objects.all().filter(plan_id=plan).order_by("order")

        days = set()
        for day in day_ids:
            days.add(DayName.objects.get(pk=day[0]))

        ctx = {
            "plan": plan,
            "days": days,
            "recipe_plans": recipe_plans,
        }
        return render(request, "app-details-schedules.html", ctx)


class PlanAddRecipe(View):
    def get(self, request):
        plans = Plan.objects.all().order_by("name")
        recipes = Recipe.objects.all().order_by("name")
        days = DayName.objects.all().order_by("day")

        ctx = {
            "plans": plans,
            "recipes": recipes,
            "days": days,
        }

        if request.session.get("error"):
            request.session["error"] = False
            ctx = {**ctx, "error": "Wypełnij poprawnie wszystkie pola"}
            return render(request, "app-schedules-meal-recipe.html", ctx)
        return render(request, "app-schedules-meal-recipe.html", ctx)

    def post(self, request):
        plan = Plan.objects.get(name=request.POST.get("plan"))
        meal_name = request.POST.get("name")
        recipe = Recipe.objects.get(name=request.POST.get("recipe"))
        day = DayName.objects.get(day=request.POST.get("day"))

        try:
            order = int(request.POST.get("number"))
        except ValueError:
            request.session["error"] = True
            return redirect('plan-add-recipe')

        RecipePlan.objects.create(plan=plan, order=order, meal_name=meal_name, recipe=recipe, day=day)

        if plan and meal_name and order and recipe and day:
            return redirect('plan-id', id=plan.id)

        request.session["error"] = True
        return redirect('plan-add-recipe')


class RecipesListView(View):
    def get(self, request):
        recipes_list = Recipe.objects.all().order_by("-votes", "-created")
        paginator = Paginator(recipes_list, 50)
        page = request.GET.get('page')

        recipes = paginator.get_page(page)

        ctx = {
            "recipes": recipes,
        }
        return render(request, "app-recipes.html", ctx)


class NewPlan(View):
    def get(self, reqeust):
        return render(reqeust, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")

        if name and description:
            plan = Plan.objects.create(name=name, description=description)
            return redirect('plan-id', id=plan.id)
        return render(request, "app-add-schedules.html", {"error": "Wypełnij poprawnie wszystkie pola"})


class PlansListView(View):
    def get(self, request):
        plans_list = Plan.objects.all().order_by("name")
        paginator = Paginator(plans_list, 50)
        page = request.GET.get('page')

        plans = paginator.get_page(page)

        ctx = {
            "plans": plans,
        }
        return render(request, "app-schedules.html", ctx)


class Contact(View):
    def get(self, request):
        if Page.objects.filter(slug="contact").exists():

            return render(request, "contact.html")
        else:
            return redirect(reverse('landing_page'))


class AboutApp(View):
    def get(self, request):
        if Page.objects.filter(slug="about_app").exists():

            return render(request, "about_app.html")
        else:
            return redirect(reverse('landing_page'))


class DeleteRecipeView(View):

    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        recipeplan = RecipePlan.objects.all().filter(recipe_id=recipe)
        recipeplan.delete()
        return redirect("plan-id", id=id)

class EditPlanView(View):
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        return render(request, "app-edit-schedules.html", {"plan": plan})

    def post(self, request, id):
        name = request.POST.get("name")
        description = request.POST.get("description")

        if name and description:
            plan = Plan.objects.get(id=id)
            plan.name = name
            plan.description = description
            plan.save()
            return redirect('plan-list')
        return redirect('edit-plan-id', id=id)
