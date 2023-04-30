from django.db import models
from django.urls import reverse
class Course(models.Model):
    c_id=models.IntegerField
    title=models.CharField(max_length=255, verbose_name="Заголовок")
    slug=models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    image=models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Изображение")
    content=models.TextField(blank=True, verbose_name="Текст")
    author=models.TextField(blank=True, verbose_name="Автор")
    time_create=models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    time_update=models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null = True, verbose_name="Категории")
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('course', kwargs={'cour_slug': self.slug})

    class Meta:
        verbose_name_plural = 'Известные курсы'
        ordering = ['id']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name = "Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    class Meta:
        verbose_name_plural = 'Категории'
        ordering = ['id']