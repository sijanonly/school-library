# -*- coding: utf-8 -*-
# @Author: sijanonly
# @Date:   2017-08-13 17:19:25
# @Last Modified by:   sijanonly
# @Last Modified time: 2017-08-18 13:41:46
import pytest

from users.models import User


@pytest.fixture
def user():
    return User(
        username='testuser',
        email='testuser@gmail.com', first_name='Test', last_name='User')


@pytest.mark.django_db
def test_get_full_name(user):

    # ACT
    full_name = user.get_full_name()

    # ASSERT
    assert full_name == 'Test User'





@pytest.mark.django_db
def test_create_user(user):
    assert isinstance(user, User)


@pytest.mark.django_db
def test_default_user_is_active(user):
    assert user.is_active


@pytest.mark.django_db
def test_default_user_is_not_staff(user):
    assert not user.is_staff


@pytest.mark.django_db
def test_default_user_is_not_superuser(user):
    assert not user.is_superuser
