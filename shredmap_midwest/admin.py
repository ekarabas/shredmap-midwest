from django.contrib import admin
from .models import User, Resort, Review

# Register your models here.
admin.site.register(User)
admin.site.register(Resort)
admin.site.register(Review)
