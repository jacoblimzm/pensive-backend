from django.contrib import admin
from .models import BlogEntry, Category
# Register your models here.
# if you don't you won't be able to add/edit/delete your models in the admin panel
from django_summernote.admin import SummernoteModelAdmin


class BlogEntryAdmin(SummernoteModelAdmin):
    exclude = ("slug",)
    list_display = ("id", "slug", "title", "category", "created_on", "breaking")
    list_display_links = ("id", "title")
    search_fields = ("title", )
    list_per_page = 20
    summernote_fields = ('content',) # specifically targeting the "content" TextField() in BlogEntry model

admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(Category)


