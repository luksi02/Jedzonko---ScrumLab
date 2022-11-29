"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jedzonko.views import (
    IndexHtmlView,
    DashboardView,
    RecipesListView,
    RecipeIdView,
    RecipeModify,
    RecipeAdd,
    PlanIdView,
    NewPlan,
    PlanAddRecipe,
    PlansListView,
    Contact,
    AboutApp,
    DeleteRecipeView,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexHtmlView.as_view()),
    path('main/', DashboardView.as_view(), name='dashboard'),
    path('recipe/<int:id>/', RecipeIdView.as_view(), name='recipe-id'),
    path('recipe/add/', RecipeAdd.as_view(), name='recipe-add'),
    path('recipe/modify/<int:id>', RecipeModify.as_view(), name='recipe-modify'),
    path('recipe/list/', RecipesListView.as_view(), name='recipes-list'),
    path('plan/<int:id>/', PlanIdView.as_view(), name='plan-id'),
    path('plan/add/', NewPlan.as_view(), name='new-plan'),
    path('plan/add-recipe/', PlanAddRecipe.as_view(), name='plan-add-recipe'),
    path('plan/list/', PlansListView.as_view(), name='plan-list'),
    path('delete-recipe/<int:id>/', DeleteRecipeView.as_view(), name='delete-recipe-id'),
    path('edit-plan/<int:id>/', EditPlanView.as_view(), name='edit-plan-id'),
    path('contact/', Contact.as_view(), name='contact'),
    path('about_app/', AboutApp.as_view(), name='about_app'),
]
