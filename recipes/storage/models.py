# storage/models.py
from django.db import models

class IngredientModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class RecipeModel(models.Model):
    name = models.CharField(max_length=255)
    elaboration = models.TextField()

class RecipeIngredientModel(models.Model):
    recipe = models.ForeignKey(RecipeModel, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(IngredientModel, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
