# storehouse/forms.py

from django import forms
from .models import StorehouseRecord

class StorehouseRecordForm(forms.ModelForm):
    class Meta:
        model = StorehouseRecord
        fields = '__all__'
