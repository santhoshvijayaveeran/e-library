import re
import requests
from django.core.management.base import BaseCommand
from book.models import Book

GUTENDEX_API = "https://gutendex.com/books/{}"

# Manual category mapping - title keyword match panni better category kudukurathu
CATEGORY_MAP = {
    "alice": "Fantasy",
    "wonderful wizard of oz": "Fantasy",
    "tom sawyer": "Adventure",
    "huckleberry finn": "Adventure",
    "frankenstein": "Horror",
    "tale of two cities": "Historical Fiction",
    "treasure island": "Adventure",
    "picture of dorian gray": "Gothic Fiction",
    "dracula": "Horror",
    "souls of black folk": "Non-Fiction",
    "little women": "Classic Fiction",
    "wuthering heights": "Romance",
    "importance of being earnest": "Comedy",
    "the prince": "Political Philosophy",
    "jane eyre": "Romance",
    "pride and prejudice": "Romance",
    "great expectations": "Classic Fiction",
    "adventures of sherlock": "Mystery",
    "yellow wallpaper": "Short Story",
    "sign of the four": "Mystery",
    "doll": "Drama",
    "crime and punishment": "Psychological Fiction",
    "moby dick": "Adventure",
}


def guess_category(title):
    lower_title = title.lower()
    for key, category in CATEGORY_MAP.items():
        if key in lower_title:
            return category
    return "Classics"


class Command(BaseCommand):
    help = "Existing books ku better category assign pannurathu (title match panni)"

    def handle(self, *args, **options):
        updated = 0
        for book in Book.objects.all():
            new_category = guess_category(book.title)
            if book.category != new_category:
                old = book.category
                book.category = new_category
                book.save(update_fields=['category'])
                self.stdout.write(self.style.SUCCESS(f"{book.title}: '{old}' -> '{new_category}'"))
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"\nDone! {updated} books updated."))
