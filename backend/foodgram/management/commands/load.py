from django.core.management import BaseCommand
import json
from foodgram.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/ingredients.json', 'rb') as f:
            data = json.load(f)
            for i in data:
                Ingredient.objects.create(
                    name=i.get('name'), measurement_unit=i.get('measurement_unit'))
