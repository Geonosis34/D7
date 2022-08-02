from django.contrib import admin
from .models import Category, News, CategorySubscribers, PostCategory

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'author', 'dateCreation', 'category', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subscribers', )

admin.site.register(Category)
admin.site.register(News)
admin.site.register(CategorySubscribers)
admin.site.register(PostCategory)