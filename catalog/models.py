from django.db import models
from django.urls import reverse
import uuid
from django.utils.translation import gettext_lazy as _
from django.db.models import PROTECT
from . import constants
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=constants.MAX_GENRE_NAME_LENGTH,
        help_text=_("Enter a book genre (e.g. Science Fiction)"),
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy)."""
    title = models.CharField(max_length=constants.MAX_BOOK_TITLE_LENGTH)
    author = models.ForeignKey(
        "Author", on_delete=PROTECT
    )
    summary = models.TextField(
        max_length=constants.MAX_BOOK_SUMMARY_LENGTH,
        help_text=_("Enter a brief description of the book"),
    )
    isbn = models.CharField(
        "ISBN",
        max_length=constants.MAX_ISBN_LENGTH,
        unique=True,
        help_text=_("13 Character ISBN number"),
    )
    genre = models.ManyToManyField(
        Genre, help_text=_("Select a genre for this book")
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. Required for displaying in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_("Unique ID for this particular book across whole library"),
    )
    book = models.ForeignKey("Book", on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=constants.MAX_BOOK_IMPRINT_LENGTH)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=constants.LOAN_STATUS,
        blank=True,
        default="m",
        help_text=_("Book availability"),
    )

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f"{self.id} ({self.book.title})"

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=constants.MAX_AUTHOR_NAME_LENGTH)
    last_name = models.CharField(max_length=constants.MAX_AUTHOR_NAME_LENGTH)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(_("Died"), null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
