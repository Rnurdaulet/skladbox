# storehouse/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_record, name='create_record'),
    path('records/', views.record_list, name='record_list'),
    path('records/<int:pk>/', views.record_detail, name='record_detail'),
]

