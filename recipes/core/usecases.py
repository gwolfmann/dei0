from recipes.storage.models import IngredientModel
from recipes.core.entities import Ingredient, Recipe
from typing import List

def create_recipe(name, ingredients, elaboration):
    # Implement business logic for creating a recipe
    # Validate data and perform any necessary operations
    return Recipe(name, ingredients, elaboration)

def create_ingredient(name,description):
    return Ingredient(name,description)

class ReadIngredientUseCase:
    def get_by_name(self, name) -> Ingredient:
        try:
            # Use Django's ORM to retrieve an ingredient by name
            ingredient_model = IngredientModel.objects.get(name=name)

            # Create an Ingredient entity from the retrieved model data
            ingredient_entity = Ingredient(
                name=ingredient_model.name,
                description=ingredient_model.description,
            )

            return ingredient_entity
        except IngredientModel.DoesNotExist:
            # If the ingredient does not exist, return None or handle the case as needed
            return None
        
    def get_by_id(self, ingredient_id) -> Ingredient:
        try:
            # Use Django's ORM to retrieve an ingredient by ID
            ingredient_model = IngredientModel.objects.get(id=ingredient_id)

            # Create an Ingredient entity from the retrieved model data
            ingredient_entity = Ingredient(
                name=ingredient_model.name,
                description=ingredient_model.description,
            )

            return ingredient_entity
        except IngredientModel.DoesNotExist:
            # If the ingredient does not exist, return None or handle the case as needed
            return None        
        
    def get_all(self) -> List[Ingredient]:
        # Use Django's ORM to retrieve all ingredients
        ingredient_models = IngredientModel.objects.all()

        # Create a list of Ingredient entities from the retrieved model data
        ingredient_entities = [
            Ingredient(
                name=ingredient_model.name,
                description=ingredient_model.description,
            )
            for ingredient_model in ingredient_models
        ]

        return ingredient_entities
    
class UpdateIngredientUseCase:
    def update(self, ingredient, ingredient_id, new_name, new_description) -> Ingredient:
        try:
            # Retrieve the original ingredient from the database by ID
            original_ingredient_model = IngredientModel.objects.get(id=ingredient_id)

            # Check if an ingredient with the same name already exists
            existing_ingredient = IngredientModel.objects.exclude(id=ingredient_id).filter(name=new_name)

            if existing_ingredient.exists():
                raise ValueError("An ingredient with the same name already exists.")

            # Update the ingredient entity
            ingredient.name = new_name
            ingredient.description = new_description

            # Update the corresponding IngredientModel in the database
            original_ingredient_model.name = new_name
            original_ingredient_model.description = new_description
            original_ingredient_model.save()

            return ingredient
        except IngredientModel.DoesNotExist:
            raise ValueError("Ingredient not found.")
        
class DeleteIngredientUseCase:
    def delete(self, ingredient_id):
        try:
            # Retrieve the ingredient to be deleted
            ingredient_model = IngredientModel.objects.get(id=ingredient_id)

            # Delete the ingredient from the database
            ingredient_model.delete()
        except IngredientModel.DoesNotExist:
            raise ValueError("Ingredient not found.")