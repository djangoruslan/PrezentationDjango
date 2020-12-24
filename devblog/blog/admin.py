from django.contrib import admin

from .models import Post, PostCategory, AdvancedUser


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_time')
    list_filter = ('category', 'author')
    search_fields = ['title', 'text']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views',)


@admin.register(PostCategory)
class CategoryPostAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(AdvancedUser)