from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from unidecode import unidecode
from users.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Perfume.Status.PUBLISHED)


class Perfume(models.Model):
    """Основная модель продукта"""
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Название парфюма')
    slug = models.SlugField(max_length=255, blank=True, unique=True, verbose_name='Slug (Формируется автоматически)')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Фото")
    content = models.TextField(blank=True, verbose_name='Описание')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                blank=True, default=100, verbose_name='Цена')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления статьи')
    cat = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True,
                            related_name='posts', verbose_name="Категории")
    tags = models.ManyToManyField('Tags', blank=True, related_name='tags', verbose_name="Теги")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Парфюм'
        verbose_name_plural = 'Парфюмы'
        ordering = ['-time_create']

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        transliterated_title = unidecode(str(self.title))
        self.slug = slugify(transliterated_title)
        super().save(*args, **kwargs)


class Category(models.Model):
    cat_name = models.CharField(max_length=255, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug (Формируется автоматически)')

    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Tags(models.Model):
    tag_name = models.CharField(max_length=255, db_index=True, verbose_name='Тег')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug (Формируется автоматически)')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class Review(models.Model):
    """Модель отзывов"""
    user_review = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    review = models.TextField(blank=True, verbose_name='Отзыв', null=True)
    product_review = models.ForeignKey(Perfume, on_delete=models.CASCADE, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.review

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Basket(models.Model):
    """Модель  корзины"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ник')
    product = models.ForeignKey(Perfume, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"Корзина для {self.user.username} | {self.product.title}"

    def total_amount(self):
        """Подсчет общей суммы товара количество * цена товара"""
        return self.quantity * self.product.price
