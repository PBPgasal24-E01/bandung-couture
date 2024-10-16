from django.core.management.base import BaseCommand
from stores.models import Store, Category
import csv

class Command(BaseCommand):
    help = 'Clears the database and loads initial dataset'

    def handle(self, *args, **kwargs):

        with open('initial-dataset.csv', mode='r', newline='') as file:
            csv_reader = csv.reader(file)

            dataset = list(csv_reader)

        Category.objects.all().delete()
        Store.objects.all().delete()

        categories_set = set()

        for i in range(len(dataset)):
            if i == 0:
                continue
            data = dataset[i]
            categories = data[2].split(',')

            for category in categories:
                categories_set.add(category)

        for category in categories_set:
            Category.objects.create(name=category)

        for i in range(len(dataset)):
            if i == 0:
                continue
            data = dataset[i]

            brand = data[0]
            description = data[1]
            categories = data[2]
            address = data[3]
            contact_number = data[4]
            website = data[5]
            social_media = data[6]

            store = Store.objects.create(brand=brand, description=description, address=address, contact_number=contact_number,
                                 website=website, social_media=social_media)
        
            for category in categories.split(','):
                category_instance = Category.objects.get(name=category)
                store.categories.add(category_instance)
                store.save()