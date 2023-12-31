from rest_framework import serializers
from .models import User, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            firstname=validated_data["firstname"],
            lastname=validated_data["lastname"],
            phone=validated_data["phone"],
            group=validated_data["group"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["group"] = instance.group.name if instance.group else None
        return representation


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")
