from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'info'

urlpatterns = [
    path('about/', views.about_company, name='about_company'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('faq/', views.faq, name='faq'),
    path('vacancies/', views.vacancies_view, name='vacancies'),
    path('news/', views.news_view, name='news'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)