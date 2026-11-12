from django.core.management.base import BaseCommand
from book.models import Category

CATEGORIES = [
    "Classic Fiction",
    "Gothic Fiction / Horror",
    "Mystery / Detective",
    "Adventure",
    "Romance",
    "Fantasy",
    "Fairy Tales",
    "Drama / Plays",
    "Comedy",
    "Historical Fiction",
    "Biographical / Autobiographical Fiction",
    "Psychological Fiction",
    "Non-Fiction",
    "Political Science / Philosophy",
    "Feminist Fiction",
    "Bildungsroman (Coming-of-age)",
    "Epistolary Fiction",
    "Short Story",
]

class Command(BaseCommand):
    help = "Seed the 18 reduced Category rows"

    def handle(self, *args, **options):
        created = 0
        for name in CATEGORIES:
            obj, was_created = Category.objects.get_or_create(name=name)
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} new categories (total {len(CATEGORIES)})"))
