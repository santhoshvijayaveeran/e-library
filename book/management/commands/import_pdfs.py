import os
import re
import requests
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from book.models import Book
from book.models import Book, Category

from django.core.management.base import BaseCommand
from django.utils.text import slugify

def get_or_create_category(category_name):
    slug = slugify(category_name)
    category_obj, created = Category.objects.get_or_create(
        slug=slug,
        defaults={"name": category_name.strip()},
    )
    return category_obj, created

GUTENDEX_API = "https://gutendex.com/books/{}"
COVER_URL_TEMPLATES = [
    "https://www.gutenberg.org/cache/epub/{}/pg{}.cover.medium.jpg",
    "https://www.gutenberg.org/cache/epub/{}/pg{}.cover.small.jpg",
]


def extract_gutenberg_id(filename):
    match = re.match(r'^(\d+)[_\-]', filename)
    return match.group(1) if match else None


def clean_title(filename):
    name = filename.rsplit('.', 1)[0]
    name = re.sub(r'^\d+[_\-]?', '', name)
    name = name.replace('_', ' ')
    name = re.sub(r'\s+', ' ', name).strip()
    return name.rstrip(' -')


def fetch_metadata(gutenberg_id):
    """Gutendex API la irundhu title, author, description edukurathu"""
    try:
        resp = requests.get(GUTENDEX_API.format(gutenberg_id), timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        title = data.get('title', '').strip()
        authors = data.get('authors', [])
        author = authors[0]['name'] if authors else "Unknown"
        subjects = data.get('subjects', [])
        category = subjects[0].split(' -- ')[0] if subjects else "Classics"
        summary_list = data.get('summaries', [])
        description = summary_list[0] if summary_list else ""
        return {
            'title': title,
            'author': author,
            'category': category,
            'description': description,
        }
    except requests.RequestException:
        return None


def fetch_cover_image(gutenberg_id):
    """Gutenberg standard cover URL la irundhu image download pannurathu"""
    for template in COVER_URL_TEMPLATES:
        url = template.format(gutenberg_id, gutenberg_id)
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200 and resp.content:
                return resp.content
        except requests.RequestException:
            continue
    return None


class Command(BaseCommand):
    help = "PDF folder scan panni Gutendex API metadata + cover image kooda Book records create pannum"

    def add_arguments(self, parser):
        parser.add_argument('folder_path', type=str, help='PDF files irukra folder path')
        parser.add_argument('--category', type=str, default=None, help='Fixed category (skip panna API category use aagum)')
        parser.add_argument('--price', type=float, default=0, help='Default price')
        parser.add_argument('--status', type=str, default='available', help='available/issued/lost')
        parser.add_argument('--added-by', type=str, default=None, help='Username - added_by field ku')

    def handle(self, *args, **options):
        folder_path = os.path.expanduser(options['folder_path'])
        fixed_category = options['category']
        price = options['price']
        status = options['status']
        added_by_username = options['added_by']

        added_by_user = None
        if added_by_username:
            added_by_user = User.objects.filter(username=added_by_username).first()
            if not added_by_user:
                self.stdout.write(self.style.WARNING(f"User '{added_by_username}' illa - added_by empty ah vidum"))

        if not os.path.isdir(folder_path):
            self.stdout.write(self.style.ERROR(f"Folder illa: {folder_path}"))
            return

        created_count = 0
        skipped_count = 0

        for filename in sorted(os.listdir(folder_path)):
            if not filename.lower().endswith('.pdf'):
                continue

            gutenberg_id = extract_gutenberg_id(filename)
            fallback_title = clean_title(filename)

            meta = fetch_metadata(gutenberg_id) if gutenberg_id else None

            title = meta['title'] if meta else fallback_title
            author = meta['author'] if meta else "Unknown"
            category_name = fixed_category or (meta['category'] if meta else "Classics")
            category_obj, _ = get_or_create_category(category_name)
            description = meta['description'] if meta else ""

            if Book.objects.filter(title=title).exists():
                self.stdout.write(self.style.WARNING(f"Skip (already exist): {title}"))
                skipped_count += 1
                continue

            full_path = os.path.join(folder_path, filename)

            book = Book(
                title=title,
                author=author,
                isbn=None,  # Gutenberg public domain books ku ISBN irukathu
                category=category_obj,  
                description=description,
                price=price,
                status=status,
                is_paid=price > 0,
                added_by=added_by_user,
            )

            # PDF file attach pannurathu
            with open(full_path, 'rb') as f:
                book.pdf_file.save(filename, File(f), save=False)

            # Cover image download panni attach pannurathu
            if gutenberg_id:
                cover_bytes = fetch_cover_image(gutenberg_id)
                if cover_bytes:
                    book.cover_image.save(
                        f"{gutenberg_id}_cover.jpg",
                        ContentFile(cover_bytes),
                        save=False
                    )
                else:
                    self.stdout.write(self.style.WARNING(f"Cover kidaikala: {title}"))

            book.save()
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Added: {title} by {author}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! {created_count} books added, {skipped_count} skipped."
        ))
