from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    inventory_number = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["owner"] = instance.owner.email if instance.owner else None
        return representation


class OrderStatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("status",)


class LibrarianOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("inventory_number", "status")
