# -*- coding: utf-8 -*-
# @Author: sijanonly
# @Date:   2017-08-12 14:00:59
# @Last Modified by:   sijanonly
# @Last Modified time: 2017-08-12 17:31:14


from rest_framework import serializers

from library.models import (
    Book, Tag, Publisher, Author, BookType)


class BookTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookType


class TagSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField('get_tag_name')

    class Meta:
        model = Tag
        fields = ('text',)

    def get_tag_name(self, obj):
        return obj.name


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author


class BookDetailSerializer(serializers.ModelSerializer):
    keywords = TagSerializer(many=True)
    publisher = PublisherSerializer(read_only=True)
    book_type = BookTypeSerializer(read_only=True)
    authors = PublisherSerializer(many=True)
    # student = serializers.SerializerMethodField('get_book_issue')

    class Meta:
        model = Book
        fields = (
            'id', 'title', 'subject',
            'ISBN', 'publisher', 'authors',
            'edition', 'availability', 'keywords',
            'number_of_copies',
            'barcode', 'book_type',
            'language',)
        read_only_fields = ('date_created', 'date_modified')
