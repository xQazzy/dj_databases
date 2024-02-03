from django.urls import path
from .views import book_list, book_detail, prev_date_books, next_date_books

urlpatterns = [
    path('', book_list, name='book_list'),
    path('<str:pub_date>/', book_list, name='book_list_by_date'),
    path('<str:pub_date>/<int:page>/', book_list, name='book_list_by_date_paginated'),
    path('<str:pub_date>/', prev_date_books, name='prev_date_books'),
    path('<str:pub_date>/', next_date_books, name='next_date_books'),
    path('detail/<str:pub_date>/', book_detail, name='book_detail'),
]
