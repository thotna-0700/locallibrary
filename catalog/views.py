from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance
from catalog.constants import (
    LOAN_STATUS_AVAILABLE,
    BOOK_PAGINATE_BY,
    LOAN_STATUS_ON_LOAN
)


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


class BookListView(generic.ListView):
    model = Book
    paginate_by = BOOK_PAGINATE_BY


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_instances"] = BookInstance.objects.filter(book=self.object)
        context["book_genres"] = self.object.genre.all()  
        context["AVAILABLE"] = LOAN_STATUS_AVAILABLE
        context["ON_LOAN"] = LOAN_STATUS_ON_LOAN
        context["MAINTENANCE"] = "m"
        return context
