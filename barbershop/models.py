from django.db import models
from django.db.models import Avg

# Мастер
class Master(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    contact_info = models.TextField(verbose_name="Контактная информация")
    photo = models.ImageField(upload_to='masters/', verbose_name="Фотография")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_rating(self):
        approved_reviews = self.reviews.filter(is_approved=True)
        if approved_reviews.exists():
            return round(approved_reviews.aggregate(Avg('rating'))['rating__avg'], 1)
        return 0

# Услуга
class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    duration = models.IntegerField(default=60, verbose_name="Длительность в минутах")
    masters = models.ManyToManyField(Master, related_name='services', verbose_name="Мастера")

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


# Запись на услугу
class Visit(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Мастер")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    date = models.DateTimeField(verbose_name="Дата и время визита")

    def __str__(self):
        return f"{self.name} - {self.service.name} ({self.date})"


# Отзывы к мастерам
class MasterReview(models.Model):
    RATING_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='reviews', verbose_name="Мастер")
    author = models.CharField(max_length=100, verbose_name="Имя автора")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отзыв от {self.author} о мастере {self.master}"
