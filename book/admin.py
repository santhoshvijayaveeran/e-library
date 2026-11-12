from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Book, Category
from .models import UserProfile, Book, IssuedBook
from .models import (
    UserProfile, Book, IssuedBook, Review, Wishlist, Order,
    Discount, Coupon, CouponUsage
)
from django.contrib import admin
from .models import ContactMessage

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone')

    def get_phone(self, obj):
        return getattr(obj.profile, 'phone_number', '-')
    get_phone.short_description = 'Phone'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at')
    search_fields = ('user__username', 'phone_number')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'book_count')
    search_fields = ('name',)

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = "Books" 


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'status', 'added_by', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'author', 'isbn')
    list_editable = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('category',)   # ADD THIS

@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'issued_to', 'issue_date', 'return_date', 'returned')
    list_filter = ('returned', 'issue_date')
    search_fields = ('book__title', 'issued_to__username')
    list_editable = ('returned',)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('book', 'discount_type', 'value', 'is_active', 'is_valid', 'start_date', 'end_date')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('book__title',)
    autocomplete_fields = ('book',)

    def is_valid(self, obj):
        return obj.is_valid
    is_valid.boolean = True


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'discount_type', 'value', 'min_purchase_amount',
        'usage_limit', 'times_used', 'is_active', 'valid_from', 'valid_until'
    )
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code',)
    readonly_fields = ('times_used',)


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'user', 'order', 'discount_amount', 'used_at')
    list_filter = ('coupon',)
    search_fields = ('user__username', 'coupon__code')
    readonly_fields = ('used_at',)



@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        # Messages come from the contact form only, not created manually
        return False
    

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'user__username', 'comment')
    autocomplete_fields = ('book', 'user')
    readonly_fields = ('created_at',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at')
    search_fields = ('user__username', 'book__title')
    autocomplete_fields = ('user', 'book')
    readonly_fields = ('created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'book', 'amount', 'status', 'coupon',
        'discount_amount', 'razorpay_order_id', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'user__username', 'book__title',
        'razorpay_order_id', 'razorpay_payment_id'
    )
    autocomplete_fields = ('user', 'book', 'coupon')
    readonly_fields = ('created_at',)


@admin.register(MyLibrary)
class MyLibraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'added_at')
    search_fields = ('user__username', 'book__title')
    autocomplete_fields = ('user', 'book')
    readonly_fields = ('added_at',)