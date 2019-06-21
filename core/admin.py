from django.contrib import admin

from .models import User, Blog, BlogPost


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', 'password', 'email']}),
    ]
    search_fields = ['username']

admin.site.register(User, UserAdmin)


class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author']}),
    ]

admin.site.register(Blog, BlogAdmin)


class BlogPostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['blog', 'title', 'text', 'image', 'pub_date', 'published']}),
    ]
    list_filter = ['pub_date']
    search_fields = ['title', 'text']

admin.site.register(BlogPost, BlogPostAdmin)
