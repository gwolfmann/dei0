# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create_recipe/', views.create_recipe_view, name='create-recipe'),
    path('ingredients/delete/<int:ingredient_id>/', views.delete_ingredient_view, name='delete-ingredient'),  # New URL for deleting an ingredient
    path('ingredients/update/<int:ingredient_id>/', views.update_ingredient_view, name='update-ingredient'),  # New URL for updating an ingredient
    path('ingredients/all/', views.get_all_ingredients_view, name='get-all-ingredients'),  # New URL for all ingredients
    path('ingredients/<int:ingredient_id>/', views.get_ingredient_by_id_view, name='get-ingredient-by-id'),  # New URL
    path('ingredients/<str:name>/', views.get_ingredient_view, name='get-ingredient'),
    path('ingredients/', views.create_ingredient_view, name='ingredient-crud'),
 # URLs for recipes
    path('recipes/update/<int:recipe_id>/', views.update_recipe_view, name='update-recipe'),
    path('recipes/delete/<int:recipe_id>/', views.delete_recipe_view, name='delete-recipe'),
    path('recipes/all/', views.get_all_recipes_view, name='get-all-recipes'),
    path('recipes/<int:recipe_id>/', views.get_recipe_by_id_view, name='get-recipe-by-id'),
    path('recipes/<str:name>/', views.get_recipe_by_name_view, name='get-recipe-by-name'),
    path('recipes/', views.create_recipe_view, name='create-recipe'),
]
