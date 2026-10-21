# Python.DjangoRules.json -> "Django Rules Python" [Authorization]
# Expected: import rules.contrib.views; decorator permission_required; methods rules.has_perm + rules.test_rule
import rules
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, UpdateView
from rules.contrib.views import PermissionRequiredMixin, objectgetter, permission_required

from .models import Book


class BookDetailView(PermissionRequiredMixin, DetailView):
    model = Book
    permission_required = "books.view_book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_edit"] = rules.has_perm("books.change_book", user, self.object)
        context["is_author"] = rules.test_rule("is_book_author", user, self.object)
        return context


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ["title", "summary"]
    permission_required = "books.change_book"
    raise_exception = True


@require_POST
@permission_required("books.publish_book", fn=objectgetter(Book, "book_id"), raise_exception=True)
def publish_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.published_at = timezone.now()
    book.save(update_fields=["published_at"])
    return redirect(book)
