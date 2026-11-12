import os
import requests
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from book.models import Category


class Command(BaseCommand):
    help = "Category ku URL vachu image download panni set pannum"

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str)
        parser.add_argument('image_url', type=str)

    def handle(self, *args, **options):
        category_name = options['category_name']
        image_url = options['image_url']

        try:
            category = Category.objects.get(name__iexact=category_name)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Category '{category_name}' kidaikala"))
            return

        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SanzaLibraryBot/1.0)'
        }

        try:
            response = requests.get(image_url, headers=headers, timeout=15, stream=True)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Image download fail aachu: {e}"))
            return

        parsed_path = urlparse(image_url).path
        filename = os.path.basename(parsed_path) or f"{category.slug or category.name}.jpg"

        if '.' not in filename:
            filename += '.jpg'

        content = ContentFile(response.content)
        category.image.save(filename, content, save=True)

        self.stdout.write(self.style.SUCCESS(f"Image URL la irundhu download panni set aachu: {category.name}"))
