from django.contrib import admin

from .models.blog import Blog, BlogPost



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
