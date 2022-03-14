from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models import Article, Tag, ArticleTag
from django.core.exceptions import ValidationError


class ArticleTagInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tag = 0
        for form in self.forms:
            print(form.cleaned_data)
            if form.cleaned_data.get('is_main'):
                if main_tag > 0:
                    raise ValidationError('Основным может быть только 1 раздел')
                main_tag += 1

        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    extra = 1
    formset = ArticleTagInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_details = ['id', 'title', 'text', 'published_at']
    inlines = [ArticleTagInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_details = ['id', 'name']
