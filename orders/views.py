from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK
from users.permissions import IsStudent, IsLibrarianOrStudent
from .models import Order, ORDER_STATUS
from .serializers import OrderSerializer, LibrarianOrderSerializer
from users.models import ROLES, User


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        serializer.validated_data["owner"] = user
        books = serializer.validated_data["books"]

        for book in books:
            if book.quantity <= 0 or not book.is_possible_to_order:
                return Response({"message": f"К сожалению вы не можете забронировать книгу {book.title} на данный момент"})

        order = serializer.save()

        for book in order.books.all():
            if book.quantity <= 0 or not book.is_possible_to_order:
                continue
            book.orders_quantity += 1
            book.quantity -= 1
            book.save()

        owner_info = {
            "owner_firstname": user.firstname,
            "owner_lastname": user.lastname,
            "owner_phone": user.phone,
            "owner_group": user.group.name,
        }

        return Response({**serializer.data, **owner_info}, status=HTTP_201_CREATED)


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == ROLES[2][1]:
            return Order.objects.filter(owner=user)

        return Order.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = []
        for order_data in serializer.data:
            owner_instance = User.objects.filter(email=order_data["owner"]).first()
            owner_info = {
                "owner_firstname": owner_instance.firstname,
                "owner_lastname": owner_instance.lastname,
                "owner_phone": owner_instance.phone,
                "owner_group": owner_instance.group.name,
            }
            order_data.update(owner_info)
            data.append(order_data)
        return Response(data)


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsLibrarianOrStudent]

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user
        owner_instance = User.objects.get(pk=order.owner_id)

        if user.role == "Student":
            if user.email != owner_instance.email:
                return Response({"message": "Вы можете просматривать только свои заказы"})

        if owner_instance:
            owner_info = {
                "owner_firstname": owner_instance.firstname,
                "owner_lastname": owner_instance.lastname,
                "owner_phone": owner_instance.phone,
                "owner_group": owner_instance.group.name,
            }
        else:
            owner_info = {}

        serializer = self.get_serializer(order)
        order = serializer.data
        order.update(owner_info)

        return Response(order, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        order = self.get_object()

        if order.status not in [status[0] for status in ORDER_STATUS]:
            return Response({"error": "Неверный статус заказа"})

        if (
                request.user.role == ROLES[2][1]
                and order.status == ORDER_STATUS[0][1]
                and order.owner == request.user
        ):
            return super().put(request, *args, **kwargs)

        if request.user.status == ROLES[2][1]:
            self.serializer_class = LibrarianOrderSerializer
            return super().put(request, *args, **kwargs)

        return Response(
            {"message": "У вас нет разрешения на изменение этого заказа"},
            status=HTTP_403_FORBIDDEN,
        )

    def delete(self, request, *args, **kwargs):
        order = self.get_object()

        if (
                request.user.role == ROLES[2][1]
                and order.status == ORDER_STATUS[0][1]
                and order.owner == request.user
        ):
            order.delete()
            return Response(
                {"message": "Заказ удален успешно"}, status=HTTP_204_NO_CONTENT
            )

        if (
                request.user.role == ROLES[1][1]
                and order.status == ORDER_STATUS[2][1]
        ):
            order.delete()
            return Response(
                {"message": "Заказ удален успешно"}, status=HTTP_204_NO_CONTENT
            )

        return Response(
            {"message": "У вас нет разрешения на удаление этого заказа"}, status=HTTP_403_FORBIDDEN
        )
