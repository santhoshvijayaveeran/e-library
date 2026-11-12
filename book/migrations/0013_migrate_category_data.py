from django.db import migrations



def migrate_category_data(apps, schema_editor):
    Book = apps.get_model('book', 'Book')
    Category = apps.get_model('book', 'Category')

    for book in Book.objects.all():
        old_value = book.category
        if old_value:
            category_obj, created = Category.objects.get_or_create(
                name=old_value,
            )
            book.category_new_id = category_obj.id
            book.save(update_fields=['category_new'])


def reverse_migrate(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_add_category_new_temp'),
    ]

    operations = [
        migrations.RunPython(migrate_category_data, reverse_migrate),
    ]
