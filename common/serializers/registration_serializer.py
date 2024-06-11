from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = UserModel.objects.create_user(username=validated_data['username'],
                                             first_name=validated_data['first_name'],
                                             last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user
