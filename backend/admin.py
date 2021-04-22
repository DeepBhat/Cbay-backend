from django.contrib import admin

# Register your models here.
from .models import Chat, User, Listing, Category, Image

admin.site.register([User, Listing, Category, Image, Chat])
