# storehouse/urls.py

from django.urls import path
from . import views
from .views import generate_pdf, get_offer_view, get_archive_view, get_points

urlpatterns = [
    path('create/', views.create_record, name='create_record'),
    path('records/', views.record_list, name='record_list'),
    path('records/<int:pk>/', views.record_detail, name='record_detail'),
    path('record/<int:record_id>/pdf/', generate_pdf, name='generate_pdf'),
    path('offer-view/', get_offer_view, name='offer_view'),
    path('archive-view/', get_archive_view, name='archive_view'),
    path('points/', get_points, name='points'),
]

