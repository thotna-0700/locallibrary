from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance
from catalog.constants import (
    LOAN_STATUS_AVAILABLE,
    BOOK_PAGINATE_BY,
    LOAN_STATUS_ON_LOAN
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required


def index(request):
    """View function for home page of site."""
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status=LOAN_STATUS_AVAILABLE).count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits, 
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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/my_borrowed_books.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status=LOAN_STATUS_ON_LOAN
        ).order_by('due_back')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan_status_on_loan'] = LOAN_STATUS_ON_LOAN  
        return context


@login_required  
@permission_required('catalog.can_mark_returned', raise_exception=True)  
def mark_book_returned(request, bookinstance_id):
    """View để đánh dấu sách là đã trả."""
    from django.shortcuts import get_object_or_404, redirect
    from django.utils import timezone

    book_instance = get_object_or_404(BookInstance, pk=bookinstance_id)
    book_instance.status = LOAN_STATUS_AVAILABLE
    book_instance.due_back = None
    book_instance.borrower = None
    book_instance.save()

    return redirect('all-borrowed')  
