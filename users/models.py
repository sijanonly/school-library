# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    Model to create a User.

    :id: User uuid.
    :city: User city.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    city = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
