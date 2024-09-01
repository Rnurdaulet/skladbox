# storehouse/urls.py

from django.urls import path
from . import views
from .views import generate_pdf

urlpatterns = [
    path('create/', views.create_record, name='create_record'),
    path('records/', views.record_list, name='record_list'),
    path('records/<int:pk>/', views.record_detail, name='record_detail'),
    path('record/<int:record_id>/pdf/', generate_pdf, name='generate_pdf'),
]

