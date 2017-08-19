

# step 1 : Let us create an instance of Book. It should fail as we don't
# have Book class

# step 2 :


import pytest

from books.models import Book, Author

# If your tests need to use the database and want to use pytest
# function test approach, you need to `mark` it.

# it is a resource available to test cases
# testcases are requesting this resources by naming it in argument list


@pytest.fixture
def book():
    book = Book(title="Seto Bagh", subject='Nepali')
    book.save()
    return book


@pytest.fixture
def authors():
    authors = []
    author = Author(first_name='Daimond', last_name='Samsher')
    author.save()
    authors.append(author)
    return authors


@pytest.mark.django_db
def test_book_save(book):
    expected_output = 'Seto Bagh'
    assert book.title == expected_output


@pytest.mark.django_db
def test_book_is_represented_by_last_name_comma_first_name(book):
    expected_output = '%s, %s' % (book.title, book.subject)
    assert str(book) == expected_output


@pytest.mark.django_db
def test_book_authors_count(book, authors):
    # add authors to book object
    book.authors.add(*authors)

    expected_output = 1
    assert len(book.author_list) == expected_output
