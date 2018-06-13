from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Tag, Comment, Image


class PostAdmin(SummernoteModelAdmin):
    search_fields = ['title']
    list_filter = ['tag']
    summernote_fields = '__all__'

class ImageAdmin(admin.ModelAdmin):
    list_filter = ['post']

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Image, ImageAdmin)
