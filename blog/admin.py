from django.contrib import admin
from .models import Post, UserProfile, Comment, Team, Sport
from .forms import PostAdminForm, TeamAdminForm


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['title', 'author', 'created_date', 'published_date']
    search_fields = ['title', 'text']
    list_filter = ['created_date', 'published_date']
    ordering = ['-created_date']

class TeamAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['name', 'abbreviation', 'sport']
    search_fields = ['name', 'abbreviation']
    list_filter = ['sport']
    ordering = ['name']

admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Team, TeamAdmin)
admin.site.register(Sport)
