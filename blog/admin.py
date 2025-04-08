from django.contrib import admin
from .models import Post, UserProfile, Comment
from .forms import PostAdminForm


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['title', 'author', 'created_date', 'published_date']
    search_fields = ['title', 'text']
    list_filter = ['created_date', 'published_date']
    ordering = ['-created_date']

admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile)
admin.site.register(Comment)
