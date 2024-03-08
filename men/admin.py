from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import Perfume, Category, Tags, Basket, Review


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    fields = ["title", 'post_photo', 'photo', 'content', 'is_published', 'cat', 'tags', 'price']
    list_display = ['title', 'post_photo', 'cat', 'is_published']
    list_editable = ['is_published']
    readonly_fields = ['post_photo']
    # prepopulated_fields = {"slug": ("title",)}
    actions = ['set_draft']
    filter_horizontal = ['tags']
    save_on_top = True

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, perfume: Perfume):
        if perfume.photo:
            return mark_safe(f"<img src='{perfume.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Perfume.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации!", messages.SUCCESS)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ["cat_name", 'slug']
    prepopulated_fields = {"slug": ("cat_name",)}


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    fields = ["tag_name", "slug"]
    prepopulated_fields = {"slug": ("tag_name",)}


admin.site.register(Basket)
admin.site.register(Review)
