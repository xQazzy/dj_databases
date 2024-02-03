from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book
from django.urls import reverse
from datetime import datetime


def book_list(request, pub_date=None):
    if pub_date:
        books = Book.objects.filter(pub_date=pub_date)
    else:
        books = Book.objects.all()

    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    try:
        book_page = paginator.page(page)
    except PageNotAnInteger:
        book_page = paginator.page(1)
    except EmptyPage:
        book_page = paginator.page(paginator.num_pages)

    prev_date_books = None
    next_date_books = None
    if pub_date:
        prev_date_books = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
        next_date_books = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()

    return render(request, 'books/books_list.html', {'books': book_page, 'pub_date': pub_date, 'prev_date_books': prev_date_books, 'next_date_books': next_date_books})


def book_detail(request, pub_date):
    book = get_object_or_404(Book, pub_date=pub_date)
    return render(request, 'books/book_detail.html', {'book': book})


def prev_date_books(request, pub_date):
    prev_date = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
    if prev_date:
        return HttpResponseRedirect(f'/books/{prev_date.pub_date.strftime("%Y-%m-%d")}/')
    else:
        return HttpResponseBadRequest("Предыдущей даты нет.")

def next_date_books(request, pub_date):
    next_date = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()
    if next_date:
        return HttpResponseRedirect(reverse('next_date_books', kwargs={'pub_date': next_date.pub_date.strftime("%Y-%m-%d")}))
    else:
        return HttpResponseBadRequest("Следущей даты нет.")
