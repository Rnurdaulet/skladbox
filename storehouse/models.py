# storehouse/models.py
from django.utils import timezone
from django.db import models

class StorehouseRecord(models.Model):
    cashless_payment = models.BooleanField(default=False, verbose_name="Безналичный расчет")
    sender_name = models.CharField(max_length=255, verbose_name="ФИО отправителя")
    sender_phone = models.CharField(max_length=255, verbose_name="Номер телефона отправителя")
    receiver_name = models.CharField(max_length=255, verbose_name="ФИО получателя")
    receiver_phone = models.CharField(max_length=255, verbose_name="Номер телефона получателя")
    places_count = models.PositiveIntegerField(verbose_name="Количество мест")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Оплачено")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name="Приложить фото")
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.sender_name} -> {self.receiver_name} ({self.places_count} мест)"
