from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer class to handle the creation of a User.

    Attributes:
        full_name (TYPE): Full Name of the user
        numbers (TYPE): Phone numbers of the user
        password (TYPE): Password of the user
    """
    full_name = serializers.CharField(
        source='get_full_name', required=False, read_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email', 'full_name', 'password', 'city')
        read_only_fields = ('id', 'full_name')

    def create(self, validated_data):
        """
        Create user object

        Args:
            validated_data: The data sent from client after validation.
        """
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', None),
            last_name=validated_data.get('last_name', None),
            city=validated_data['city'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
