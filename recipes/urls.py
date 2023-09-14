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
]
