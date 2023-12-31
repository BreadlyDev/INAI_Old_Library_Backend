from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsStudent
from .models import Review
from .serializers import ReviewSerializer


class AllReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]


class ReviewListAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        book_id = self.kwargs["book_id"]
        return Review.objects.filter(book_id=book_id)


class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["author"] = request.user
        book = serializer.validated_data["book"]
        serializer.save()

        book.reviews_quantity += 1
        book.save()

        return Response(serializer.data, status=HTTP_201_CREATED)


class ReviewRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def put(self, request, *args, **kwargs):
        review = self.get_object()
        if review.author == request.user:
            return super().put(request, *args, **kwargs)

        return Response(
            {"Сообщение": "У вас нет разрешения на изменение этого отзыва"},
            status=HTTP_403_FORBIDDEN,
        )

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        if review.author == request.user:
            review.delete()
            return Response(
                {"Сообщение": "Отзыв успешно удален"}, status=HTTP_204_NO_CONTENT
            )

        return Response(
            {"Сообщение": "У вас нет разрешения на удаление этого отзыва"},
            status=HTTP_403_FORBIDDEN
        )
