# core/entities.py
class Ingredient:
    def __init__(self, name, description, id):
        self.id = id
        self.name = name
        self.description = description

class Recipe:
    def __init__(self, name, ingredients, elaboration, id):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.elaboration = elaboration
