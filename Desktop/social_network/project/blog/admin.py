from django.contrib import admin
from .models import Post, Comment, Like




class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at', 'updated_at',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at', 'updated_at',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post',)



admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
