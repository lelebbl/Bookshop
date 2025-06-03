from django.shortcuts import render, redirect
from .models import AboutCompany, FAQ, Vacancy, News
from .forms import FAQForm
import requests


def about_company(request):
    history = AboutCompany.objects.all()
    return render(request, 'info/about_company.html', {'history': history})


def privacy_policy(request):
    return render(request, 'info/privacy_policy.html')


def faq(request):
    faqs = FAQ.objects.order_by('-created_at')

    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('info:faq')  
    else:
        form = FAQForm()

    return render(request, 'info/faq.html', {'faqs': faqs, 'form': form})


def vacancies_view(request):
    vacancies = Vacancy.objects.all().order_by('-published_at')
    return render(request, 'info/vacancies.html', {'vacancies': vacancies})


def news_view(request):
    news_list = News.objects.all()
    return render(request, 'info/news.html', {'news_list': news_list})

def privacy_policy(request):
    # шутка дня
    try:
        joke_url = 'https://official-joke-api.appspot.com/random_joke'
        joke_response = requests.get(joke_url, timeout=5).json()
        joke_data = {
            'setup': joke_response['setup'],
            'punchline': joke_response['punchline']
        }
    except Exception:
        joke_data = {'error': 'Ошибка загрузки шутки'}

    # изображение кота
    try:
        cat_image_url = 'https://cataas.com/cat'
    except Exception:
        cat_image_url = None  

    return render(request, 'info/privacy_policy.html', {
        'joke': joke_data,
        'cat_image_url': cat_image_url,
    })


