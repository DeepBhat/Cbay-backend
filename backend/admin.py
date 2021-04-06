from django.contrib import admin

# Register your models here.
from .models import Chat, User, Listing, Category, Image, Transaction

admin.site.register([User, Listing, Category, Image, Chat, Transaction])
