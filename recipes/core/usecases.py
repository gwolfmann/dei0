from recipes.storage.models import IngredientModel, RecipeModel, RecipeIngredientModel
from recipes.core.entities import Ingredient, Recipe
from typing import List

def create_ingredient(name,description):
    return Ingredient(name,description)

def create_recipe(name, ingredients, elaboration):
    # Implement business logic for creating a recipe
    # Validate data and perform any necessary operations
    return Recipe(name, ingredients, elaboration)

class ReadIngredientUseCase:
    def get_by_name(self, name) -> Ingredient:
        try:
            # Use Django's ORM to retrieve an ingredient by name
            ingredient_model = IngredientModel.objects.get(name=name)

            # Create an Ingredient entity from the retrieved model data
            ingredient_entity = Ingredient(
                id=ingredient_model.id,
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
                id=ingredient_model.id,
                name=ingredient_model.name,
                description=ingredient_model.description,
            )

            return ingredient_entity
        except IngredientModel.DoesNotExist:
            # If the ingredient does not exist, return None or handle the case as needed
            return None        
        
    def get_all(self) -> List[Ingredient]:
        # Use Django's ORM to retrieve all ingredients
        ingredient_models = IngredientModel.objects.all().order_by('id')

        # Create a list of Ingredient entities from the retrieved model data
        ingredient_entities = [
            Ingredient(
                name=ingredient_model.name,
                description=ingredient_model.description,
                id=ingredient_model.id
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
        

class ReadRecipeUseCase:  
    def get_by_name(self, name) -> Recipe:
        try:
            recipe_model = RecipeModel.objects.get(name=name)
            recipe_ingredients_model = RecipeIngredientModel.objects.filter(recipe=recipe_model)
            ingredients = []
            for recipe_ingredient_model in recipe_ingredients_model:
                ingredient_entity = {
                    "id":recipe_ingredient_model.id,
                    "name": recipe_ingredient_model.ingredient.name,
                    "quantity": recipe_ingredient_model.quantity,
                }
                ingredients.append(ingredient_entity)
            recipe_entity = Recipe(
                name=recipe_model.name,
                ingredients=ingredients,
                elaboration=recipe_model.elaboration,
                id=recipe_model.id
            )
            return recipe_entity
        except RecipeModel.DoesNotExist:
            return None

    def get_by_id(self, recipe_id) -> Recipe:
        try:
            recipe_model = RecipeModel.objects.get(id=recipe_id)
            recipe_ingredients_model = RecipeIngredientModel.objects.filter(recipe=recipe_model)
            ingredients = []
            for recipe_ingredient_model in recipe_ingredients_model:
                ingredient_entity = {
                    "id":recipe_ingredient_model.id,
                    "name": recipe_ingredient_model.ingredient.name,
                    "quantity": recipe_ingredient_model.quantity,
                }
                ingredients.append(ingredient_entity)
            recipe_entity = Recipe(
                name=recipe_model.name,
                ingredients=ingredients,
                elaboration=recipe_model.elaboration,
                id=recipe_model.id
            )

            return recipe_entity
        except RecipeModel.DoesNotExist:
            return None

    def get_all(self) -> List[Recipe]:
        try:
            recipe_models = RecipeModel.objects.all().order_by('id')

            recipe_entities = []

            for recipe_model in recipe_models:
                recipe_ingredients_model = RecipeIngredientModel.objects.filter(recipe=recipe_model)
                ingredients = []
                for recipe_ingredient_model in recipe_ingredients_model:
                    ingredient_entity = {
                        "name": recipe_ingredient_model.ingredient.name,
                        "quantity": recipe_ingredient_model.quantity,
                        "id": recipe_ingredient_model.id,
                    }
                    ingredients.append(ingredient_entity)
                recipe_entities.append(Recipe(
                    name=recipe_model.name,
                    ingredients=ingredients,
                    elaboration=recipe_model.elaboration,
                    id=recipe_model.id
                ))
            return recipe_entities
        except Exception:
            return []

class UpdateRecipeUseCase:
    def update(self, recipe, recipe_id, new_name, new_ingredients, new_elaboration) -> Recipe:
        try:
            original_recipe_model = RecipeModel.objects.get(id=recipe_id)
            recipe_ingredients_model = RecipeIngredientModel.objects.filter(recipe=original_recipe_model)

            recipe.name = new_name
            recipe.ingredients = new_ingredients
            recipe.elaboration = new_elaboration

            original_recipe_model.name = new_name
            #original_recipe_model.ingredients = new_ingredients
            original_recipe_model.elaboration = new_elaboration
            original_recipe_model.save()
            for ingredient_original in recipe_ingredients_model:
                original_ingredient=IngredientModel.objects.get(id=ingredient_original.ingredient_id)
                original_ingredient.delete()
            recipe_ingredients_model.delete()
            for ingredient_data in new_ingredients:
                ingredient_model = IngredientModel(name=ingredient_data["name"],description="")
                ingredient_model.save()
                # Create and save the RecipeIngredientModel linking the recipe and ingredient
                recipe_ingredient_model = RecipeIngredientModel(recipe=original_recipe_model,
                                                            ingredient=ingredient_model,
                                                            quantity=ingredient_data["quantity"])
                recipe_ingredient_model.save()
            return recipe
        except RecipeModel.DoesNotExist:
            raise ValueError("Recipe not found.")

class DeleteRecipeUseCase:
    def delete(self, recipe_id):
        try:
            recipe_model = RecipeModel.objects.get(id=recipe_id)
            recipe_ingredients_model = RecipeIngredientModel.objects.filter(recipe=recipe_model)

            recipe_model.delete()
            recipe_ingredients_model.delete()
        except RecipeModel.DoesNotExist:
            raise ValueError("Recipe not found.")
