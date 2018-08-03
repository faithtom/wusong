from django.contrib import admin
from .models import AppDoc

class AppDocAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish", "id")
    list_filter = ("publish", "author")
    search_fields = ('title', "body")
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ['publish', 'author']

admin.site.register(AppDoc, AppDocAdmin)
