import json
from django.http import JsonResponse,HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from recipes.core.usecases import create_recipe, create_ingredient, ReadIngredientUseCase, UpdateIngredientUseCase, DeleteIngredientUseCase
from recipes.storage.repositories import IngredientRepositoryImpl
from recipes.storage.models import RecipeModel, IngredientModel
from django.views.decorators.csrf import csrf_exempt

read_ingredient_use_case = ReadIngredientUseCase()
update_ingredient_use_case = UpdateIngredientUseCase()
delete_ingredient_use_case = DeleteIngredientUseCase()

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

        # Call the domain use case to create a recipe
        recipe_entity = create_recipe(name, ingredients, elaboration)
        # Save the Recipe entity to the database
        # Note: You may need to adapt this code to save the entity properly using Django's ORM
        # For example, assuming RecipeModel is your Django model for recipes:
        recipe_model = RecipeModel(
            name=recipe_entity.name,
            ingredients=recipe_entity.ingredients,
            elaboration=recipe_entity.elaboration
        )
        recipe_model.save()
        # Return a JSON response
        return JsonResponse({
            'name': recipe_entity.name,
            'ingredients': recipe_entity.ingredients,
            'elaboration': recipe_entity.elaboration,
        }, status=201)  # HTTP status 201 indicates creation

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

        # Call the domain use case to create a recipe
        ingredient_entity = create_ingredient(name, description)
        ingredient_model = IngredientModel(
            name=ingredient_entity.name,
            description=ingredient_entity.description,
        )
        ingredient_model.save()
        # Return a JSON response
        return JsonResponse({
            'name': ingredient_entity.name,
            'description': ingredient_entity.description,
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