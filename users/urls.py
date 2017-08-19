from django.conf.urls import url

from rest_framework_jwt.views import (
    obtain_jwt_token, verify_jwt_token, refresh_jwt_token)

from .views import (UserDetails, UserList)

"""
Configure the URL patterns for the Users API.
"""
urlpatterns = [
    # Return a specific User by id
    url(
        r'^(?P<id>[0-9a-f-]+)/$',
        UserDetails.as_view(), name='user-detail'
    ),
     # Login a User
    url(
        r'^login/',
        obtain_jwt_token, name='login'
    ),
    # List all Parent Users
    url(
        r'^$',
        UserList.as_view(), name='user-list'
    ),
    # Verify a User's JWT token
    url(
        r'^token-verify/',
        verify_jwt_token
    ),
    # Refresh a User's JWT token
    url(
        r'^token-refresh/',
        refresh_jwt_token
    ),
]
