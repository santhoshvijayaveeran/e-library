from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('management/', views.management_view, name='management'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('wishlist/toggle/<int:book_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('book/<int:book_id>/review/', views.add_review, name='add_review'),
    path('book/<int:book_id>/buy/', views.buy_book, name='buy_book'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('coupon/apply/<int:book_id>/', views.apply_coupon, name='apply_coupon'),
    path('coupon/remove/<int:book_id>/', views.remove_coupon, name='remove_coupon'),
    path('order/create/<int:book_id>/', views.create_payment_order, name='create_payment_order'),
    path('book/<int:book_id>/read/', views.serve_book_pdf, name='serve_book_pdf'),
    path('accounts/ajax-login/', views.ajax_login, name='ajax_login'),
    path('categories/', views.category_home, name='category_home'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('category/<path:category_name>/', views.category_books_view, name='category_books'),
    path('books/free/', views.free_books_view, name='free_books'),
    path('books/paid/', views.paid_books_view, name='paid_books'),
    path('books/free/categories/', views.free_categories_view, name='free_categories'),
    path('books/paid/categories/', views.paid_categories_view, name='paid_categories'),
    path('books/all/', views.all_books_view, name='all_books'),
    path('books/recent/', views.recent_books_view, name='recent_books'),
    path('books/popular/', views.popular_books_view, name='popular_books'),
    path('about/', views.about, name='about'),
    path('books/', views.books_view, name='books'),
    path('my-library/', views.my_library_view, name='my_library'),
    path('my-library/toggle/<int:book_id>/', views.toggle_library, name='toggle_library'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('faq/', views.faq, name='faq'),
    path('management/author/book/add/', views.author_add_book, name='author_add_book'),
    path('management/author/book/<int:book_id>/edit/', views.author_edit_book, name='author_edit_book'),
    path('management/author/book/<int:book_id>/delete/', views.author_delete_book, name='author_delete_book'),
    path('my-library/category/<str:category_id>/', views.my_library_category_view, name='my_library_category'),

    # ============================================================
# ADD TO urls.py — alongside the author_* URLs added earlier
# ============================================================

# Books
path('management/admin/book/add/', views.admin_add_book, name='admin_add_book'),
path('management/admin/book/<int:book_id>/edit/', views.admin_edit_book, name='admin_edit_book'),
path('management/admin/book/<int:book_id>/delete/', views.admin_delete_book, name='admin_delete_book'),

# Categories
path('management/admin/category/add/', views.admin_add_category, name='admin_add_category'),
path('management/admin/category/<int:category_id>/edit/', views.admin_edit_category, name='admin_edit_category'),
path('management/admin/category/<int:category_id>/delete/', views.admin_delete_category, name='admin_delete_category'),

# Authors (entity, not user)
path('management/admin/author/add/', views.admin_add_author, name='admin_add_author'),
path('management/admin/author/<int:author_id>/edit/', views.admin_edit_author, name='admin_edit_author'),
path('management/admin/author/<int:author_id>/delete/', views.admin_delete_author, name='admin_delete_author'),

# Access management (Users)
path('management/admin/access/grant/', views.admin_grant_access, name='admin_grant_access'),
path('management/admin/access/<int:user_id>/toggle/', views.admin_toggle_access, name='admin_toggle_access'),
path('management/admin/access/<int:user_id>/remove/', views.admin_remove_access, name='admin_remove_access'),

# About Us
path('management/admin/about/save/', views.admin_save_about, name='admin_save_about'),


# ============================================================
# ALSO ADD to the top of views.py:
#   from django.db.models import Q
# (used in the admin_grant_access team query)
# ============================================================

    # allauth (Google SSO) urls
    path('accounts/', include('allauth.urls')),
]
