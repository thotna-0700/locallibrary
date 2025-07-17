from django.shortcuts import render
from catalog.models import Book, Author, BookInstance
from catalog.constants import LOAN_STATUS_AVAILABLE


def index(request):
    """View function for home page of site."""
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status=LOAN_STATUS_AVAILABLE).count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)
