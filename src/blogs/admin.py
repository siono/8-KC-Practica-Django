from django.contrib import admin

from blogs.models import Category, Blog, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_select_related = ('user',)
    list_display = ('name', 'user')
    search_fields = ('name', 'user__first_name', 'user__last_name', 'user__email', 'user__username')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'multimedia', 'summary', 'body', ('publication_date', 'blog'), 'categories')
    filter_horizontal = ('categories',)
    date_hierarchy = 'publication_date'
    search_fields = ('title', 'summary', 'body', 'blog__name')
    list_select_related = ('blog',)
    list_filter = ('categories', 'blog')
    list_display = ('title', 'blog', 'publication_date')
    save_as = True