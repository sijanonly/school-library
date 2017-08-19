# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions, status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwner

from .models import User
from .serializers import UserSerializer


class UserList(ListCreateAPIView):
    """
    post:
        Register a new User.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)

    # def post(self, request, format=None):
    #     serializer = self.serializer_class(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(
    #         serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(RetrieveUpdateDestroyAPIView):
    """
    get:
        Return a User instance.

    put:
        Update a User.

    delete:
        Delete an existing user.
    """
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated, IsOwner)
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return (permissions.IsAuthenticated(), IsOwner(),)

        if self.request.method == "DELETE":
            return (permissions.IsAuthenticated(), permissions.IsAdminUser(),)

        return (permissions.IsAuthenticated(),)
