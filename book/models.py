from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.utils import timezone





class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


class Book(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('issued', 'Issued'),
        ('lost', 'Lost'),
    )

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='books/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='books_added')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='authored_books'
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.isbn is not None and self.isbn.strip() == '':
            self.isbn = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def final_price(self):
        """Returns the discounted price if an active discount exists, otherwise the normal price."""
        if hasattr(self, 'discount') and self.discount.is_valid:
            return self.discount.get_discounted_price()
        return self.price

    @property
    def has_discount(self):
        return hasattr(self, 'discount') and self.discount.is_valid

    class Meta:
        ordering = ['-created_at']

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='author_images/', blank=True, null=True)

    def __str__(self):
        return self.name




class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issue_records')
    issued_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_books')
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} -> {self.issued_to.username}"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)  # 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.username} -> {self.book.title} ({self.rating}★)"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} wishlisted {self.book.title}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')

    # For tracking whether a coupon was applied
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.book.title} ({self.status})"


# ---------------- Discount Feature ----------------

class Discount(models.Model):
    """Book-level discount - for setting a direct discount on a single book."""

    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('flat', 'Flat Amount'),
    )

    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name='discount'
    )
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage'
    )
    value = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="0-100 if percentage, amount if flat"
    )
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.book.title} - {self.value}{'%' if self.discount_type == 'percentage' else '₹'} off"

    @property
    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True

    def get_discounted_price(self):
        original_price = self.book.price

        if not self.is_valid:
            return original_price

        if self.discount_type == 'percentage':
            discount_amount = (original_price * self.value) / 100
        else:  # flat
            discount_amount = self.value

        final_price = original_price - discount_amount
        return max(final_price, 0)


class Coupon(models.Model):
    """Coupon codes that can be applied at checkout time."""

    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('flat', 'Flat Amount'),
    )

    code = models.CharField(max_length=30, unique=True)
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage'
    )
    value = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    max_discount_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Max cap amount for percentage discount (optional)"
    )
    min_purchase_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text="Coupon only applies above this amount"
    )

    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()

    usage_limit = models.PositiveIntegerField(
        default=0,
        help_text="0 = unlimited usage"
    )
    times_used = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    def is_valid(self, purchase_amount=0):
        now = timezone.now()

        if not self.is_active:
            return False, "Coupon is inactive"
        if now < self.valid_from or now > self.valid_until:
            return False, "Coupon expired"
        if self.usage_limit > 0 and self.times_used >= self.usage_limit:
            return False, "Coupon usage limit reached"
        if purchase_amount < self.min_purchase_amount:
            return False, f"Minimum ₹{self.min_purchase_amount} purchase required"

        return True, "Valid"

    def calculate_discount(self, amount):
        if self.discount_type == 'percentage':
            discount = (amount * self.value) / 100
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        else:
            discount = self.value

        return min(discount, amount)


class CouponUsage(models.Model):
    """Tracks who used which coupon (to prevent duplicate use)."""

    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('coupon', 'user', 'order')

    def __str__(self):
        return f"{self.user} used {self.coupon.code}"
    
class MyLibrary(models.Model):
    """Tracks which free books a user has added to 'My Library'.
    Paid books automatically end up in the library via an Order (status='paid') -
    that's permanent and can't be removed. Only free books get added/removed
    through this model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library_entries')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='in_libraries')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    

# Add this to your existing models.py
class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"
    

# ============================================================
# ADD TO models.py
# ============================================================

class AboutPage(models.Model):
    """Singleton row (pk always 1) holding the editable About Us content."""
    heading = models.CharField(max_length=200, default="About Sanza Library")
    body = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # prevent accidental deletion of the singleton row

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'heading': 'About Sanza Library',
            'body': 'Sanza Library began as a single shelf and has grown into a home for readers of every kind.',
        })
        return obj

    def __str__(self):
        return self.heading