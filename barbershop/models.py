from django.db import models

class Master(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    contact_info = models.TextField(verbose_name="Контактная информация")
    photo = models.ImageField(upload_to='masters/', verbose_name="Фотография")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    masters = models.ManyToManyField(Master, related_name='services', verbose_name="Мастера")

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"

class Visit(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Мастер")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    date = models.DateTimeField(verbose_name="Дата и время визита")

    def __str__(self):
        return f"{self.name} - {self.service.name} ({self.date})"