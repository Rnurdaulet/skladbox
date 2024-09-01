from django import forms
from .models import StorehouseRecord

class StorehouseRecordForm(forms.ModelForm):
    class Meta:
        model = StorehouseRecord
        fields = [
            'cashless_payment',
            'sender_name',
            'sender_phone',
            'receiver_name',
            'receiver_phone',
            'places_count',
            'amount_paid',
            'comment',
            'photo'
        ]
        widgets = {
            'cashless_payment': forms.CheckboxInput(attrs={'class': ''}),
            'sender_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО отправителя'}),
            'sender_phone': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '+7 777 123 45 67', 'rows': 2}),
            'receiver_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО получателя'}),
            'receiver_phone': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '+7 777 123 45 67', 'rows': 2}),
            'places_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите количество мест'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'placeholder': 'Введите сумму'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите комментарий', 'rows': 3}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
