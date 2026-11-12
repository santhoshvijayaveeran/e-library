import random
from django.core.management.base import BaseCommand
from book.models import Book, Category


class Command(BaseCommand):
    help = "Admin la irukkura Category name filter panni, andha books ku 100-200 range price random ah set pannum"

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str, help='Admin la irukkura exact Category name')
        parser.add_argument('--min-price', type=float, default=100)
        parser.add_argument('--max-price', type=float, default=200)
        parser.add_argument('--only-free', action='store_true', help='Ippo price=0 irukra books ku mattum apply pannum')

    def handle(self, *args, **options):
        category_name = options['category_name']
        min_price = options['min_price']
        max_price = options['max_price']
        only_free = options['only_free']

        try:
            category = Category.objects.get(name__iexact=category_name)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Category '{category_name}' kidaikala"))
            return

        books = Book.objects.filter(category=category)
        if only_free:
            books = books.filter(price=0)

        if not books.exists():
            self.stdout.write(self.style.WARNING("Idhu category la books edhuvum kidaikala"))
            return

        updated = 0
        for book in books:
            price = round(random.uniform(min_price, max_price), 2)
            book.price = price
            book.is_paid = True
            book.save(update_fields=['price', 'is_paid'])
            updated += 1
            self.stdout.write(self.style.SUCCESS(f"{book.title} -> ₹{price}"))

        self.stdout.write(self.style.SUCCESS(f"\nDone! {updated} books updated in '{category.name}'"))