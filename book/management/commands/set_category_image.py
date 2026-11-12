import os
from django.core.files import File
from django.core.management.base import BaseCommand
from book.models import Category


class Command(BaseCommand):
    help = "Category ku local image file set pannum"

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str)
        parser.add_argument('image_path', type=str)

    def handle(self, *args, **options):
        category_name = options['category_name']
        image_path = os.path.expanduser(options['image_path'])

        try:
            category = Category.objects.get(name__iexact=category_name)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Category '{category_name}' kidaikala"))
            return

        if not os.path.isfile(image_path):
            self.stdout.write(self.style.ERROR(f"Image file kidaikala: {image_path}"))
            return

        with open(image_path, 'rb') as f:
            filename = os.path.basename(image_path)
            category.image.save(filename, File(f), save=True)

        self.stdout.write(self.style.SUCCESS(f"Image set aachu: {category.name}"))
