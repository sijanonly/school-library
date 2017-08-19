# -*- coding: utf-8 -*-
# @Author: sijanonly
# @Date:   2017-08-13 21:14:39
# @Last Modified by:   sijanonly
# @Last Modified time: 2017-08-17 13:01:51

"""
    Usage : pytest users/tests/test_api.py -s
"""

# a 401 Unauthorized response should be used for missing or
# bad authentication, and a 403 Forbidden response should be used afterwards,
# when the user is authenticated but isn’t authorized to perform
# the requested operation on the given resource.

import json

import pytest

from django.urls import reverse

from users.serializers import UserSerializer


@pytest.fixture
def user_data():
    return {'email': 'john@gmail.com',
            'username': 'john_coloney',
            'password': 'password123',
            'city': 'Cincinnati',
            'first_name': 'John',
            'last_name': 'Coloney'}


@pytest.mark.django_db
def test_valid_user_data(user_data):
    serializer = UserSerializer(data=user_data)
    is_valid = serializer.is_valid()

    assert is_valid == True




@pytest.mark.django_db
def test_login_with_empty_password_gives_bad_request(
        django_user_model, user_data, client):
    """
    Test login without password gives 400 bad request.
    """
    # Create a new user
    user = django_user_model.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'])

    login_url = reverse('users-api:login')
    response = client.post(
        login_url,
        {"username": user.username})

    expected_status = 400  # bad request
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_login_with_empty_password_gives_error_message(
        django_user_model, user_data, client):
    """
    Test login without password will give error message..
    """
    # Create a new user
    user = django_user_model.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'])

    login_url = reverse('users-api:login')
    response = client.post(
        login_url,
        {"username": user.username})

    response_content = response.content.decode('utf-8')

    assert 'This field is required.' in response_content


@pytest.mark.django_db
def test_api_can_create_a_user(user_data, client):
    """
    Test that the API has the ability to create a User.
    """
    # ARRANGE
    url = reverse('users-api:user-list')
    expected_status = 201  # created

    # ACT
    response = client.post(url, user_data)

    # ASSERT
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_invalid_email_id_gives_bad_request(user_data, client):
    """
    Test that the API has the ability raise 400 with invalid email.
    """
    # change email to invalid
    user_data['email'] = "invalid_email"
    url = reverse('users-api:user-list')
    response = client.post(url, user_data)
    expected_status = 400  # created
    assert response.status_code == expected_status, "Invalid email"


@pytest.mark.django_db
def test_invalid_email_id_gives_error_message(user_data, client):
    """
    Test that the API has the ability to raise error message
        with invalid email.
    """
    # ARRANGE
    user_data['email'] = "invalid_email"
    url = reverse('users-api:user-list')
    expected_message = 'Enter a valid email address.'

    # ACT
    response = client.post(url, user_data)

    # ASSERT
    response_content = response.content.decode('utf-8')
    assert expected_message in response_content


@pytest.mark.django_db
def test_list_user_without_authentication_is_not_allowed(client):
    """
    Test authorization is enforced while accessing user list.
    """
    # ARRANGE
    url = reverse('users-api:user-list')
    expected_status = 401  # missing authentication

    # ACT
    response = client.get(url)

    # ASSERT
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_user_listing_for_authenticated_user_is_allowed(
        django_user_model, user_data, client):
    """
    Test normal authenticated users can't access user list.
    """
    # Create a new user
    user = django_user_model.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'])

    login_url = reverse('users-api:login')
    response = client.post(
        login_url,
        {"username": user.username, "password": "password123"})

    response_content = json.loads(response.content.decode('utf-8'))
    token = response_content["token"]

    response = client.get(
        "/api/users/", {}, HTTP_AUTHORIZATION='JWT {}'.format(token))
    expected_status = 200  # success
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_normal_user_is_not_allowed_to_update_other_profile(
        django_user_model, user_data, client):
    """
    Test only owner is allowed to update his/her profile.
    """
    user = django_user_model.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'])

    # create normal user
    normal_user = django_user_model.objects.create_user(
        username='normal_user',
        email='normal_user@gmail.com',
        password='random123')

    # login as normal user
    login_url = reverse('users-api:login')
    response = client.post(
        login_url,
        {"username": normal_user.username, "password": "random123"})

    response_content = json.loads(response.content.decode('utf-8'))
    token = response_content["token"]

    # send patch request to other user update profile
    update_url = reverse('users-api:user-detail', kwargs={'id': user.id})
    response = client.patch(
        update_url,
        HTTP_AUTHORIZATION='JWT {}'.format(token),
        data={
            'first_name': 'John Viggor'
        })
    expected_status = 403  # not authorized (don't have permissions)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_owner_user_is_allowed_to_update_their_profile(
        django_user_model, user_data, client):
    """
    Test only owner is allowed to update his/her profile.
    """
    user = django_user_model.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'])

    # self login
    login_url = reverse('users-api:login')
    response = client.post(
        login_url,
        {"username": user.username, "password": "password123"})

    response_content = json.loads(response.content.decode('utf-8'))
    token = response_content["token"]

    # send patch request to update own's profile
    update_url = reverse('users-api:user-detail', kwargs={'id': user.id})
    data = json.dumps({"first_name": "Michael Faraday"})
    response = client.patch(
        update_url,
        HTTP_AUTHORIZATION='JWT {}'.format(token),
        data=data, content_type='application/json')

    # get updated user data
    get_updated_user_data = client.get(
        update_url,
        HTTP_AUTHORIZATION='JWT {}'.format(token))
    updated_user_profile = get_updated_user_data.content.decode('utf-8')

    expected_first_name = 'Michael Faraday'

    expected_status = 200  # success

    assert response.status_code == expected_status
    assert expected_first_name in updated_user_profile


@pytest.mark.django_db
def test_normal_user_is_not_allowed_to_delete_their_profile(
        django_user_model, user_data, client):
    """
    Test only owner is allowed to update his/her profile.
    """
    user = django_user_model.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'])

    # login as normal user
    login_url = reverse('users-api:login')
    response = client.post(
        login_url,
        {"username": user.username, "password": "password123"})

    response_content = json.loads(response.content.decode('utf-8'))
    token = response_content["token"]

    # send patch request to other user update profile
    update_url = reverse('users-api:user-detail', kwargs={'id': user.id})
    response = client.delete(
        update_url,
        HTTP_AUTHORIZATION='JWT {}'.format(token),
        data={'format': 'John json'})
    expected_status = 403  # not authorized (don't have permissions)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_staff_user_allowed_to_delete_user_profile(
        django_user_model, user_data, client):
    """
    Test only owner is allowed to update his/her profile.
    """
    user = django_user_model.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'])
    # update user as staff user

    # create staff user
    staff_user = django_user_model.objects.create_user(
        username='normal_user',
        email='normal_user@gmail.com',
        password='random123')
    staff_user.is_staff = True
    staff_user.save()

    # login as staff user
    login_url = reverse('users-api:login')
    response = client.post(
        login_url,
        {"username": staff_user.username, "password": "random123"})

    response_content = json.loads(response.content.decode('utf-8'))
    token = response_content["token"]

    # send patch request to other user update profile
    update_url = reverse('users-api:user-detail', kwargs={'id': user.id})
    response = client.delete(
        update_url,
        HTTP_AUTHORIZATION='JWT {}'.format(token),
        data={'format': 'John json'})

    expected_status = 204  # no content
    assert django_user_model.objects.count() == 1
    assert response.status_code == expected_status
