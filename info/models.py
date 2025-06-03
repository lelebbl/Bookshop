from django.db import models


class AboutCompany(models.Model):
    year = models.PositiveIntegerField()
    event = models.TextField()

    class Meta:
        ordering = ['year']
        verbose_name = 'Company Event'
        verbose_name_plural = 'Company Events'
        

    def __str__(self):
        return f"{self.year}: {self.event[:50]}"
    

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.TextField(blank=True, verbose_name="Ответ")  # blank=True позволяет оставить пустым
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.question
    

class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name="Изображение")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title