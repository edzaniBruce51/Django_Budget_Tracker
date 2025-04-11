from django.contrib import admin
from .models import Category, Expense, Budget

# Simple admin registration without custom admin classes
# This provides basic admin functionality without excess code
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Budget)
