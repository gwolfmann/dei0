# core/entities.py
class Ingredient:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Recipe:
    def __init__(self, name, ingredients, elaboration):
        self.name = name
        self.ingredients = ingredients
        self.elaboration = elaboration
