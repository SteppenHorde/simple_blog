from django.contrib import admin

from .models.blog import Blog, BlogPost



class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author', 'subscribers']}),
    ]

admin.site.register(Blog, BlogAdmin)


class BlogPostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['blog', 'read', 'title', 'text', 'image', 'pub_date']}),
    ]
    list_filter = ['pub_date']
    search_fields = ['title', 'text']

admin.site.register(BlogPost, BlogPostAdmin)
