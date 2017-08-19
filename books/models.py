# -*- coding: utf-8 -*-

"""Models representing a library books and their relations
"""
# @Author: sijanonly
# @Date:   2017-08-11 10:44:00
# @Last Modified by:   sijanonly
# @Last Modified time: 2017-08-12 22:03:59


from autoslug import AutoSlugField

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Tag(models.Model):
    """
    Tags for book (e.g. computer-science, economics).

    """

    # Attributes:
    name = models.CharField(unique=True, max_length=60)
    slug = AutoSlugField(
        populate_from='name', always_update=True, unique=True)

    # Meta and Strings:
    class Meta:

        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        """
        String for representing the Tag object.
        """
        return self.name


class Publisher(models.Model):
    """

    Publisher records of a book.

    """

    # Attributes:
    name = models.CharField(max_length=50)
    publication_year = models.IntegerField(
        ('Publication Year'),
        blank=True,
        null=True
    )
    publication_place = models.CharField(
        max_length=200, blank=True, null=True)

    # Meta and Strings:
    class Meta:
        get_latest_by = "name"
        ordering = ['name']
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")

    def __str__(self):
        """
        String for representing the Publisher object.
        """
        return self.name


class Author(models.Model):
    """
    Auther records for a book.

    """

    # Attributes:
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Meta and Strings:
    class Meta:
        get_latest_by = "name"
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        """
        String for representing the Author object.
        """
        return self.name

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


class BookType(models.Model):
    """
    Stores book type.

    Users can borrow books from library for different
    time period. This class defines frequently-used
    lending periods. (reference books, lending books)


    """

    # Attributes:
    name = models.CharField(max_length=50)
    days_amount = models.IntegerField(blank=True, null=True)

    # Meta and Strings:
    class Meta:
        get_latest_by = "days_amount"
        ordering = ['days_amount']
        verbose_name = _("Book Type")
        verbose_name_plural = _("Book Types")

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    """

    A book record.

    """

    # Relations:
    publisher = models.ForeignKey(
        Publisher,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='book_publisher'
    )
    book_type = models.ForeignKey(
        BookType,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='book_lend_type'
    )
    # Many to many relation is used because a book can have many,
    # many authors
    authors = models.ManyToManyField(
        Author,
        blank=True,
        verbose_name=("Book Authors"),
        related_name='book_author'
    )
    keywords = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='book_tag'
    )

    # Attributes:
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, blank=True)
    language = models.CharField(max_length=100, blank=True)
    availability = models.BooleanField(default=False)
    status = models.TextField(blank=True)
    number_of_copies = models.IntegerField(blank=True, null=True)
    barcode = models.CharField(
        max_length=50,
        verbose_name=('Barcode'),
        unique=True,
        blank=True, null=True
    )

    # Meta and Strings:
    class Meta:

        ordering = ['created']
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return '%s, %s' % (self.title, self.subject)

    @property
    def author_list(self):
        """
        A list of authors for a book object.

        """
        return [a.full_name for a in self.authors.all()]

    @property
    def year_published(self):
        """
        Book published year.

        """
        return self.publisher.publication_year

    def check_barcode(self, code):
        """
        Checks if a barcode already used or not.

        Args:
            code (string): barcode to be checked.

        Returns:
            bool: returns true if barcode already exists else false.
        """
        pass
