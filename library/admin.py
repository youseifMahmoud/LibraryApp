"""
Registering the Book and Author models to make them manageable 
through the Django admin interface.

"""
from django.contrib import admin
from .models import Book, Author

admin.site.register(Book)
admin.site.register(Author)
