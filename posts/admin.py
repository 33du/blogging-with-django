from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Tag, Comment


class PostAdmin(SummernoteModelAdmin):
    search_fields = ['title']
    list_filter = ['tag']
    summernote_fields = '__all__'


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
