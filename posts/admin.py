from django.contrib import admin

from .models import Post, Tag, Comment, Image


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['tag']

class ImageAdmin(admin.ModelAdmin):
    list_filter = ['post']

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Image, ImageAdmin)
