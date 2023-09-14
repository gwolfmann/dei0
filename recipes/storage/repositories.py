# storage/repositories.py
from recipes.core.entities import Ingredient
from recipes.storage.models import IngredientModel

class IngredientRepositoryImpl:
    def get_by_name(self, name):
        try:
            ingredient_model = IngredientModel.objects.get(name=name)
            return Ingredient(ingredient_model.name, ingredient_model.description)
        except IngredientModel.DoesNotExist:
            return None  # Handle the case when the ingredient is not found
