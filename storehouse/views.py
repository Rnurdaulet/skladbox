# storehouse/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import StorehouseRecordForm
from .models import StorehouseRecord
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string

def generate_pdf(request, record_id):
    # Получаем данные из модели
    record = get_object_or_404(StorehouseRecord, id=record_id)

    # Рендерим HTML-шаблон с данными
    html_string = render_to_string('template.html', {'record': record})

    # Опции для wkhtmltopdf
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'no-outline': None
    }

    # Генерация PDF
    pdf = pdfkit.from_string(html_string, False, options=options)

    # Возвращаем PDF в виде HTTP-ответа
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="record_{record_id}.pdf"'

    return response


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