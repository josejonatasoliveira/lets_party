from django.contrib import admin
from .models import TopicCategory, TopicType
# Register your models here.


class TopicCategoryAdmin(admin.ModelAdmin):
    model = TopicCategory
    list_display_links = ('identifier',)
    list_display = (
        'identifier',
        'description',
        'fa_class')
    search_fields=('description',)

class TopicTypeAdmin(admin.ModelAdmin):
    model = TopicType
    list_display_links = ('identifier',)
    list_display = (
        'identifier',
        'description',
        'fa_class')
    search_fields=('description',)

admin.site.register(TopicCategory)
admin.site.register(TopicType)
