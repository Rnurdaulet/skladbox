from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class StorehouseRecord(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Принято'),
        ('delivered', 'Доставлено'),
        ('issued', 'Выдано'),
    ]

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

    # Новые поля
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='accepted', verbose_name="Статус")
    created_by = models.ForeignKey(User, related_name='created_records', on_delete=models.SET_NULL, null=True,
                                   verbose_name="Создано пользователем")
    updated_by = models.ForeignKey(User, related_name='updated_records', on_delete=models.SET_NULL, null=True,
                                   verbose_name="Обновлено пользователем")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления статуса")

    def __str__(self):
        return f"{self.sender_name} -> {self.receiver_name} ({self.places_count} мест, статус: {self.get_status_display()})"

class StatusHistory(models.Model):
    storehouse_record = models.ForeignKey(StorehouseRecord, related_name='status_history', on_delete=models.CASCADE)
    old_status = models.CharField(max_length=10, choices=StorehouseRecord.STATUS_CHOICES)
    new_status = models.CharField(max_length=10, choices=StorehouseRecord.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Изменено пользователем")
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"Статус изменен с {self.old_status} на {self.new_status} пользователем {self.changed_by}"
