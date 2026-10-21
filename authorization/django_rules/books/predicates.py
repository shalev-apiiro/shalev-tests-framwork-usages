# Python.DjangoRules.json -> "Django Rules Python" [Authorization]
# Expected: none (predicate definitions only; models.py, admin.py, api.py and views.py carry the matches)
import rules


@rules.predicate
def is_book_author(user, book):
    return book is not None and book.author_id == user.id


@rules.predicate
def is_editor(user):
    return user.groups.filter(name="editors").exists()


rules.add_rule("is_book_author", is_book_author)
