from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()

    context = {'books': books}
    return render(request, template, context)

def books_by_date(request, book_date):
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('pub_date')

    current_books = Book.objects.filter(pub_date=book_date)

    paginator = Paginator(books, len(current_books))
    current_page = list(books).index(current_books[0]) + 1
    page = paginator.page(current_page)

    context = {'books': current_books,
               'page': page,}
    previous_book = Book.objects.filter(pub_date__lt=book_date).order_by('-pub_date')
    if len(previous_book) > 0:
        previous_date = str(previous_book[0].pub_date)
        context['previous_date'] = previous_date

    next_book = Book.objects.filter(pub_date__gt=book_date).order_by('pub_date')
    if len(next_book) > 0:
        next_date = str(next_book[0].pub_date)
        context['next_date'] = next_date

    return render(request, template, context)


