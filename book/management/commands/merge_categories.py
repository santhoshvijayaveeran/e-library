from django.core.management.base import BaseCommand
from django.db import transaction
from book.models import Category, Book

CATEGORY_MAP = {
    "Belgians": "Historical Fiction",
    "Frankenstein's monster (Fictitious character)": "Gothic Fiction / Horror",
    "Metamorphosis": "Fantasy",
    "Autobiographical fiction": "Biographical / Autobiographical Fiction",
    "Courage": "Non-Fiction",
    "Causation": "Political Science / Philosophy",
    "African Americans": "Historical Fiction",
    "Dostoyevsky, Fyodor, 1821-1881": "Biographical / Autobiographical Fiction",
    "Dracula, Count (Fictitious character)": "Gothic Fiction / Horror",
    "Political science": "Political Science / Philosophy",
    "Corporal punishment": "Non-Fiction",
    "Dublin (Ireland)": "Historical Fiction",
    "Brothers": "Psychological Fiction",
    "Abduction": "Mystery / Detective",
    "Aristocracy (Social class)": "Historical Fiction",
    "Fairy tales": "Fairy Tales",
    "Crime": "Mystery / Detective",
    "Man-woman relationships": "Romance",
    "Brahmans": "Historical Fiction",
    "Astrologers": "Non-Fiction",
    "Arnold, Thomas, 1795-1842": "Historical Fiction",
    "Adultery": "Romance",
    "Chastelard, Pierre de Bocosel de, 1540-1562": "Romance",
    "Adventure stories, English": "Adventure",
    "France": "Historical Fiction",
    "Comedy plays": "Comedy",
    "Faust, -approximately 1540": "Gothic Fiction / Horror",
    "Africa": "Historical Fiction",
    "Chance": "Political Science / Philosophy",
    "Children": "Psychological Fiction",
    "Epistolary fiction": "Epistolary Fiction",
    "Hawaii": "Historical Fiction",
    "American fiction": "Classic Fiction",
    "Frederick II, King of Prussia, 1712-1786": "Historical Fiction",
    "Acadians": "Historical Fiction",
    "Optimism": "Political Science / Philosophy",
    "Satire": "Comedy",
    "Feminist fiction": "Feminist Fiction",
    "Banks and banking": "Non-Fiction",
    "Appearance (Philosophy)": "Psychological Fiction",
    "Detective and mystery stories, English": "Mystery / Detective",
    "British": "Classic Fiction",
    "Domestic fiction": "Classic Fiction",
    "Burglars": "Mystery / Detective",
    "Denmark": "Historical Fiction",
    "Conflict of generations": "Psychological Fiction",
    "Classical literature": "Classic Fiction",
    "Detective and mystery stories": "Mystery / Detective",
    "French fiction": "Classic Fiction",
    "England": "Historical Fiction",
    "Benefactors": "Biographical / Autobiographical Fiction",
    "Great Britain": "Historical Fiction",
    "Biographical fiction": "Biographical / Autobiographical Fiction",
    "Pirates": "Adventure",
    "Adventure stories": "Adventure",
    "Beresford, Tommy (Fictitious character)": "Mystery / Detective",
    "Copyists": "Non-Fiction",
    "Ireland": "Historical Fiction",
    "Courtship": "Romance",
    "Herodias": "Drama / Plays",
    "Bildungsromans": "Bildungsroman (Coming-of-age)",
    "Individuality": "Psychological Fiction",
    "Political ethics": "Political Science / Philosophy",
    "Evolution (Biology)": "Non-Fiction",
    "Alice (Fictitious character from Carroll)": "Fantasy",
    "Classics": "Classic Fiction",
    "Political Philosophy": "Political Science / Philosophy",
    "Gothic Fiction": "Gothic Fiction / Horror",
    "Short Story": "Short Story",
    "Mystery": "Mystery / Detective",
    "Drama": "Drama / Plays",
    "Psychological Fiction": "Psychological Fiction",
    "Non-Fiction": "Non-Fiction",
    "Classic Fiction": "Classic Fiction",
    "Fantasy": "Fantasy",
    "Romance": "Romance",
    "Adventure": "Adventure",
    "Comedy": "Comedy",
    "Horror": "Gothic Fiction / Horror",
    "Historical Fiction": "Historical Fiction",
}

class Command(BaseCommand):
    help = "Merge 80 raw Category rows into 18 reduced Category rows and reassign books"

    def handle(self, *args, **options):
        with transaction.atomic():
            moved = 0
            deleted = 0
            for old_name, new_name in CATEGORY_MAP.items():
                old_cat = Category.objects.filter(name=old_name).first()
                if not old_cat:
                    continue
                new_cat, _ = Category.objects.get_or_create(name=new_name)
                count = Book.objects.filter(category=old_cat).update(category=new_cat)
                moved += count
                if old_cat.id != new_cat.id:
                    old_cat.delete()
                    deleted += 1
            self.stdout.write(self.style.SUCCESS(f"Moved {moved} books, deleted {deleted} old categories"))
