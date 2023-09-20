import json
from django.http import JsonResponse,HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from recipes.core.usecases import create_recipe, create_ingredient, ReadIngredientUseCase, UpdateIngredientUseCase, DeleteIngredientUseCase, ReadRecipeUseCase, UpdateRecipeUseCase,DeleteRecipeUseCase
from recipes.storage.models import RecipeModel, IngredientModel, RecipeIngredientModel
from django.views.decorators.csrf import csrf_exempt

read_ingredient_use_case = ReadIngredientUseCase()
update_ingredient_use_case = UpdateIngredientUseCase()
delete_ingredient_use_case = DeleteIngredientUseCase()
read_recipe_use_case = ReadRecipeUseCase()
update_recipe_use_case = UpdateRecipeUseCase()
delete_recipe_use_case = DeleteRecipeUseCase()

@csrf_exempt
def create_ingredient_view(request):
    if request.method == 'POST':
        # Extract JSON data from the request
        try:
            json_data = json.loads(request.body)
            name = json_data['name']
            description = json_data['description']
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        ingredient_model = IngredientModel(
            name=name,
            description=description,
        )
        ingredient_model.save()
        # Return a JSON response
        return JsonResponse({
            'name': ingredient_model.name,
            'description': ingredient_model.description,
        }, status=201)  # HTTP status 201 indicates creation

@csrf_exempt
def get_ingredient_view(request, name):
    if request.method == 'GET':
        # Use the read use case to retrieve an ingredient by name
        ingredient_entity = read_ingredient_use_case.get_by_name(name)

        if not ingredient_entity:
            return JsonResponse({'error': 'Ingredient not found'}, status=404)

        # Return a JSON response
        return JsonResponse({
            'name': ingredient_entity.name,
            'description': ingredient_entity.description,
        })
    return HttpResponseBadRequest("Invalid request method.")

@csrf_exempt
def get_ingredient_by_id_view(request, ingredient_id):
    if request.method == 'GET':
        try:
            print("ingredient id",ingredient_id)
            # Use the read use case to retrieve an ingredient by ID
            ingredient_entity = read_ingredient_use_case.get_by_id(ingredient_id)

            if not ingredient_entity:
                return HttpResponseNotFound("Ingredient not found in database")

            # Return a JSON response
            return JsonResponse({
                'id': ingredient_id,
                'name': ingredient_entity.name,
                'description': ingredient_entity.description,
            })
        except ValueError:
            return HttpResponseBadRequest("Invalid ingredient ID")
    return HttpResponseBadRequest("Invalid request method.")

@csrf_exempt
def get_all_ingredients_view(request):
    if request.method == 'GET':
        # Use the read use case to retrieve all ingredients
        ingredient_entities = read_ingredient_use_case.get_all()

        # Create a list of dictionaries from the ingredient entities
        ingredients_data = [
            {
                'id': ingredient.id,
                'name': ingredient.name,
                'description': ingredient.description,
            }
            for ingredient in ingredient_entities
        ]

        # Return a JSON response with all ingredients
        return JsonResponse(ingredients_data, safe=False)
    return HttpResponseBadRequest("Invalid request method.")

@csrf_exempt
def update_ingredient_view(request, ingredient_id):
    if request.method == 'PUT':  # You can use PUT or PATCH depending on your API design
        try:
            # Use the read use case to retrieve an ingredient by ID
            ingredient_entity = read_ingredient_use_case.get_by_id(ingredient_id)

            if not ingredient_entity:
                return HttpResponseNotFound("Ingredient not found")

            try:
                data = json.loads(request.body)
                new_name = data.get('new_name')
                new_description = data.get('new_description')
            except json.JSONDecodeError:
                return HttpResponseBadRequest("Invalid JSON data in the request body")

            if not new_name:
                return HttpResponseBadRequest("New name is required.")

            # Use the update use case to update the ingredient
            updated_ingredient_entity = update_ingredient_use_case.update(
                ingredient_entity, ingredient_id, new_name, new_description)

            # Return a JSON response with the updated ingredient data
            return JsonResponse({
                'id': ingredient_id,
                'name': updated_ingredient_entity.name,
                'description': updated_ingredient_entity.description,
            })
        except ValueError:
            return HttpResponseBadRequest("Invalid ingredient ID")
    return HttpResponseBadRequest("Invalid request method.")

@csrf_exempt
def delete_ingredient_view(request, ingredient_id):
    if request.method == 'DELETE':
        try:
            # Use the delete use case to delete the ingredient by ID
            delete_ingredient_use_case.delete(ingredient_id)

            # Return a success response
            return  JsonResponse({ 'ingredient_id': ingredient_id }, status=204)  

        except ValueError:
            return HttpResponseBadRequest("Invalid ingredient ID")
    return HttpResponseBadRequest("Invalid request method.")

# Get a recipe by ID
@csrf_exempt
def create_recipe_view(request):
    if request.method == 'POST':
        # Extract JSON data from the request
        try:
            json_data = json.loads(request.body)
            name = json_data['name']
            ingredients = json_data['ingredients']
            elaboration = json_data['elaboration']
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        recipe_model = RecipeModel(
            name=name,
            elaboration=elaboration
        )
        recipe_model.save()
        for ingredient_data in ingredients:
            ingredient_model = IngredientModel(name=ingredient_data["name"],description="",id=ingredient_data["ingredient_id"])
            #ingredient_model.save()
            # Create and save the RecipeIngredientModel linking the recipe and ingredient
            recipe_ingredient_model = RecipeIngredientModel(recipe=recipe_model,
                                                            ingredient=ingredient_model,
                                                            quantity=ingredient_data["quantity"],
                                                            id=ingredient_model.id)
            recipe_ingredient_model.save()
        # Return a JSON response
        return JsonResponse({
            'name': name,
            'ingredients': ingredients,
            'elaboration': elaboration,
        }, status=201)  # HTTP status 201 indicates creation

@csrf_exempt
def get_recipe_by_id_view(request, recipe_id):
    if request.method == 'GET':
        try:
            recipe = read_recipe_use_case.get_by_id(recipe_id)
            if recipe:
                return JsonResponse({
                    'id':recipe.id,
                    'name': recipe.name,
                    'ingredients': recipe.ingredients,
                    'elaboration': recipe.elaboration,
                })
            else:
                return HttpResponseNotFound("Recipe not found")
        except Exception as e:
            return HttpResponseServerError(str(e))
    return HttpResponseBadRequest("Invalid request method.")

# Get a recipe by name
@csrf_exempt
def get_recipe_by_name_view(request, name):
    if request.method == 'GET':
        try:
            recipe = read_recipe_use_case.get_by_name(name)
            if recipe:
                return JsonResponse({
                    'id':recipe.id,
                    'name': recipe.name,
                    'ingredients': recipe.ingredients,
                    'elaboration': recipe.elaboration,
                })
            else:
                return HttpResponseNotFound("Recipe not found")
        except Exception as e:
            return HttpResponseServerError(str(e))
    return HttpResponseBadRequest("Invalid request method.")

# Update a recipe by ID
@csrf_exempt
def update_recipe_view(request, recipe_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            new_name = data.get('new_name')
            new_ingredients = data.get('new_ingredients')
            new_elaboration = data.get('new_elaboration')

            if not new_name or not new_ingredients or not new_elaboration:
                return HttpResponseBadRequest("Missing required fields.")

            recipe = read_recipe_use_case.get_by_id(recipe_id)
            if not recipe:
                return HttpResponseNotFound("Recipe not found")

            updated_recipe = update_recipe_use_case.update(recipe, recipe_id, new_name, new_ingredients, new_elaboration)

            return JsonResponse({
                'name': updated_recipe.name,
                'ingredients': updated_recipe.ingredients,
                'elaboration': updated_recipe.elaboration,
            })
        except Exception as e:
            return HttpResponseServerError(str(e))
    return HttpResponseBadRequest("Invalid request method.")

# Delete a recipe by ID
@csrf_exempt
def delete_recipe_view(request, recipe_id):
    if request.method == 'DELETE':
        try:
            delete_recipe_use_case.delete(recipe_id)
            return JsonResponse({"result":f"Receipe {recipe_id} deleted"}, status=204)
        except Exception as e:
            return HttpResponseServerError(str(e))
    return HttpResponseBadRequest("Invalid request method.")

# Get all recipes
@csrf_exempt
def get_all_recipes_view(request):
    if request.method == 'GET':
        try:
            recipes = read_recipe_use_case.get_all()
            recipe_data = [
                {
                    'name': recipe.name,
                    'ingredients': recipe.ingredients,
                    'elaboration': recipe.elaboration,
                    'id': recipe.id
                }
                for recipe in recipes
            ]
            return JsonResponse(recipe_data, safe=False)
        except Exception as e:
            return HttpResponseServerError(str(e))
    return HttpResponseBadRequest("Invalid request method.")
