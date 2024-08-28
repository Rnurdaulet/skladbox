# storehouse/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import StorehouseRecordForm
from .models import StorehouseRecord

def create_record(request):
    if request.method == 'POST':
        form = StorehouseRecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('record_list')  # нужно будет создать URL для списка записей
    else:
        form = StorehouseRecordForm()
    return render(request, 'storehouse/create_record.html', {'form': form})

def record_list(request):
    records = StorehouseRecord.objects.all()
    return render(request, 'storehouse/record_list.html', {'records': records})

def record_detail(request, pk):
    record = get_object_or_404(StorehouseRecord, pk=pk)
    return render(request, 'storehouse/record_detail.html', {'record': record})