from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import QuerySet


from service.models import User, Comments, Post


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name_user", "phone", "date_joined")
    list_filter = ("date_joined",)
    search_fields = ["first_name", "last_name"]
    actions = ["close_status", "delete_book"]


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("text", "author_link", "created_at")
    search_fields = ["title", "author"]
    actions = ["close_status"]

    def author_link(self, obj):
        auth = obj.author
        url = reverse("admin:service_user_changelist") + str(auth.pk)
        return format_html(f'<a href="{url}">{auth}</a>')

    author_link.short_description = 'Автор'


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author_link", "created_at")
    list_filter = ("created_at",)
    search_fields = ["title"]

    def author_link(self, obj):
        auth = obj.author
        url = reverse("admin:service_user_changelist") + str(auth.pk)
        return format_html(f'<a href="{url}">{auth}</a>')

    author_link.short_description = 'Автор'


admin.site.register(User, UserAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Post, PostAdmin)
