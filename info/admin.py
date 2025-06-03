from django.contrib import admin
from .models import AboutCompany, FAQ, Vacancy, News


@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    list_display = ('year', 'event')
    ordering = ('year',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    search_fields = ('title',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')    
    search_fields = ('title', 'content')         
    list_filter = ('published_at',)       