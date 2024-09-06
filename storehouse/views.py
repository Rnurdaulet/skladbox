from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StorehouseRecordForm
from .models import StorehouseRecord, StatusHistory
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string

@login_required
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

@login_required
def create_record(request):
    if request.method == 'POST':
        form = StorehouseRecordForm(request.POST, request.FILES)
        if form.is_valid():
            # Создаем объект, но пока не сохраняем его в базу данных
            record = form.save(commit=False)
            # Устанавливаем пользователя, который создал запись
            record.created_by = request.user
            # Устанавливаем начальный статус
            record.status = 'accepted'
            # Сохраняем запись
            record.save()

            # Сохраняем историю изменения статуса
            StatusHistory.objects.create(
                storehouse_record=record,
                old_status='',
                new_status='accepted',
                changed_by=request.user
            )

            return redirect('record_list')  # нужно будет создать URL для списка записей
    else:
        form = StorehouseRecordForm()

    return render(request, 'storehouse/create_record.html', {'form': form})

@login_required
def update_status(request, record_id):
    record = get_object_or_404(StorehouseRecord, id=record_id)
    old_status = record.status
    new_status = request.POST.get('status')  # Получаем новый статус из формы

    if new_status and new_status != old_status:
        # Обновляем статус
        record.status = new_status
        record.updated_by = request.user
        record.save()

        # Записываем изменения в историю
        StatusHistory.objects.create(
            storehouse_record=record,
            old_status=old_status,
            new_status=new_status,
            changed_by=request.user
        )

    # Изменяем ключевой аргумент на 'pk' для правильного перенаправления
    return redirect('record_detail', pk=record.id)

@login_required
def record_list(request):
    status = request.GET.get('status')  # Получаем статус из параметров запроса
    if status:
        records = StorehouseRecord.objects.filter(status=status)
    else:
        records = StorehouseRecord.objects.all()  # Если статус не указан, выводим все записи

    return render(request, 'storehouse/record_list.html', {'records': records, 'current_status': status})

@login_required
def record_detail(request, pk):
    record = get_object_or_404(StorehouseRecord, pk=pk)
    return render(request, 'storehouse/record_detail.html', {'record': record})

@login_required
def edit_record(request, pk):
    record = get_object_or_404(StorehouseRecord, pk=pk)
    old_status = record.status  # Сохраняем старый статус до изменений

    if request.method == 'POST':
        form = StorehouseRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            new_status = form.cleaned_data['status']  # Получаем новый статус из формы
            if new_status != old_status:
                # Если статус изменён, записываем изменения в историю
                StatusHistory.objects.create(
                    storehouse_record=record,
                    old_status=old_status,
                    new_status=new_status,
                    changed_by=request.user
                )
            form.save()  # Сохраняем изменения записи
            return redirect('record_detail', pk=record.pk)
    else:
        form = StorehouseRecordForm(instance=record)

    return render(request, 'storehouse/edit_record.html', {'form': form, 'record': record})


