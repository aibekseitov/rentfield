import uuid

from rest_framework.serializers import ModelSerializer
from Auth.models import User, Profile


class ProfileReadSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ProfileWriteSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('type','phone_number','email')

class ProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone_number','email')

class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class UserWriteSerializer(ModelSerializer):
    profile = ProfileWriteSerializer()
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        token = uuid.uuid4()
        Profile.objects.create(user=user, token=token, **profile)
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance