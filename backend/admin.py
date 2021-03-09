from django.contrib import admin

# Register your models here.
from .models import User, Listing, Category, Image

admin.site.register(User, Listing, Category, Image)
