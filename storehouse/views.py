# storehouse/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import StorehouseRecordForm
from .models import StorehouseRecord
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.contrib.staticfiles import finders

def generate_pdf(request, record_id):
    record = get_object_or_404(StorehouseRecord, id=record_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="record_{record_id}.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Регистрация шрифта
    font_path = finders.find('fonts/DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
    pdf.setFont("DejaVuSans", 12)

    # Заполнение PDF контентом
    pdf.drawString(2 * cm, height - 2 * cm, f"Получатель: {record.receiver_name}")
    pdf.drawString(2 * cm, height - 3 * cm, f"Кол-во мест: {record.places_count}")
    pdf.drawString(2 * cm, height - 4 * cm, f"Оплата: {record.amount_paid}")
    pdf.drawString(2 * cm, height - 5 * cm, f"Дата: {record.date.strftime('%d.%m.%Y')}")

    # Добавление изображения
    image_path = finders.find('pdf.jpg')
    if image_path:
        pdf.drawImage(image_path, 2 * cm, height - 12 * cm, width=16 * cm, preserveAspectRatio=True)
    else:
        pdf.drawString(2 * cm, height - 12 * cm, "Изображение не найдено")

    pdf.showPage()
    pdf.save()

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