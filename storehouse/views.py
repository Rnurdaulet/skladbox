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

import requests
from django.http import JsonResponse

USERNAME = 'sks_techno@mail.ru'
PASSWORD = 'Password1'
HEADERS = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, как Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'
}
M_PARAM = '18604100'


def get_kaspi_cookies():
    login_url = 'https://kaspi.kz/mc/api/login'
    params = {
        'username': USERNAME,
        'password': PASSWORD
    }

    try:
        response = requests.post(login_url, params=params,
                                 headers={k: v.encode('utf-8') if isinstance(v, str) else v for k, v in
                                          HEADERS.items()})
        if response.status_code == 200:
            return response.cookies
        else:
            print(f"Failed to login. Status code: {response.status_code}, Response: {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request exception: {str(e)}")
        return None


def make_kaspi_request(url, params, headers, cookies):
    try:
        response = requests.get(url, params=params,
                                headers={k: v.encode('utf-8') if isinstance(v, str) else v for k, v in
                                         headers.items()}, cookies=cookies)

        if response.status_code == 200:
            return response.json(), 200
        else:
            return {'error': f'Failed to get data from Kaspi API. Status code: {response.status_code}'}, response.status_code
    except requests.RequestException as e:
        return {'error': f'An exception occurred: {str(e)}'}, 500


def fetch_kaspi_data(view_url, params):
    cookies = get_kaspi_cookies()

    if cookies is None:
        return JsonResponse({'error': 'Failed to get cookies from Kaspi API'}, status=500)

    result, status_code = make_kaspi_request(view_url, params, HEADERS, cookies)
    return JsonResponse(result, status=status_code if status_code != 200 else 200, safe=False)


def get_offer_view(request):
    print("Starting get_offer_view")
    offer_view_url = 'https://mc.shop.kaspi.kz/bff/offer-view/list'
    params = {
        'm': M_PARAM,
        'p': 0,
        'l': 10,
        'a': 'true',
        't': '',
        'c': ''
    }
    print("Params prepared:", params)

    response = fetch_kaspi_data(offer_view_url, params)
    print("Response received:", response)

    return response

def get_archive_view(request):
    archive_view_url = 'https://mc.shop.kaspi.kz/mc/api/orderTabs/archive'
    params = {
        'start': 0,
        'count': 10,
        'fromDate': 1722970800000,
        'toDate': 1723027971803,
        'statuses': ['CANCELLED', 'COMPLETED', 'RETURNED', 'CREDIT_TERMINATION_PROCESS'],
        '_m': M_PARAM
    }
    return fetch_kaspi_data(archive_view_url, params)


def get_points(request):
    points_url = 'https://mc.shop.kaspi.kz/bff/points'
    params = {
        'merchantUid': M_PARAM
    }
    return fetch_kaspi_data(points_url, params)

# (selected_tab = PICKUP,SIGN_REQUIRED,NEW,DELIVERY,
#  KASPI_DELIVERY_WAIT_FOR_POINT_DELIVERY,KASPI_DELIVERY_CARGO_ASSEMBLY,
#  KASPI_DELIVERY_WAIT_FOR_COURIER,KASPI_DELIVERY_TRANSMITTED,KASPI_DELIVERY_RETURN_REQUEST)
def get_active_orders(request, selected_tab):
    active_orders_url = 'https://mc.shop.kaspi.kz/mc/api/orderTabs/active'
    params = {
        'count': 10,
        'selectedTabs': selected_tab,
        'startIndex': 0,
        '_m': M_PARAM
    }
    return fetch_kaspi_data(active_orders_url, params)