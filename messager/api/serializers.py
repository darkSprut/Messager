from rest_framework.serializers import ModelSerializer
from auth_app.models import Profile, Avatar
from django.contrib.auth.models import User


class AvatarSerializer(ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Avatar


class UserSerializers(ModelSerializer):

    class Meta:
        fields = "pk", "username",
        model = User


class ProfileSerializer(ModelSerializer):
    user = UserSerializers(many=False)
    avatar = AvatarSerializer(many=False)

    class Meta:
        fields = "user", "name", "age", "bio", "avatar", "created_at",
        model = Profile


class ProfileSimpleSerializer(ModelSerializer):

    class Meta:
        fields = "name", "age", "bio",
        model = Profile


class ErrorsSerializer:
    def __init__(self, data):
        self._data = data
        self._serialize_data = self.serialize()

    def serialize(self):
        error_dict = {"errors": {}}
        for key in self._data.keys():
            error_dict["errors"][key] = self._data.get(key)[0].title()
        return error_dict

    def data(self):
        return self._serialize_data