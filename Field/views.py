from rest_framework import mixins
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import list_route

from rest_framework.permissions import AllowAny, IsAdminUser, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Auth.permissions import IsManager
from Field.models import Field, Timetable, UserLikes
from Field.serializers import FieldWriteSerializer, FieldReadSerializer, TimetableSerializer, LikeSerializer


class FieldViewSet(ModelViewSet):
    """
    retrieve:
        Показывает field по указанному id
    create:
        Создаёт field. Возрващает field после создания
    delete:
        Удаляет field по указанному id
    empty:
        Показывает клиенту пустые field'ы \n
        Доступна только для администратора Django
    """
    queryset = Field.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self, *args, **kwargs):
        """
        Если тип запроса GET, HEAD, OPTIONS, то изменяет serializer
        """
        if self.request.method in SAFE_METHODS:
            return FieldReadSerializer
        return FieldWriteSerializer

    @list_route(methods=["post"], permission_classes=[IsManager,IsAuthenticated])
    def create_field(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        serializer = FieldWriteSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @list_route(methods=["get"], permission_classes=[AllowAny])
    def active(self, request):
        queryset = Field.objects.only_active()
        serializer = self.get_serializer(queryset,many = True)
        return Response(serializer.data)

    @list_route(methods=["get"], permission_classes=[AllowAny])
    def booked(self, request):
        queryset = Timetable.objects.booked(request)
        serializer = TimetableSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=["get"], permission_classes=[AllowAny])
    def manager_fields(self, request):
        queryset = Field.objects.filter(owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=["post"], permission_classes=[IsAuthenticated])
    def put_like(self, request):
        if (Field.objects.filter(id=request.data['field']).count() > 0):
            field = Field.objects.get(id=request.data['field'])
            if (UserLikes.objects.filter(user=request.user, field=field).count() == 0):
                UserLikes(user=request.user, field=field).save()
                field.likes += 1
                field.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN, data={"message" : "You can like each field only once."})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=["get"], permission_classes=[AllowAny])
    def get_likes(self, request):
        serializer = LikeSerializer(Field.objects.values_list('id','likes'), many=True)
        serializer.is_valid()
        return Response(status=status.HTTP_200_OK, data = serializer.validated_data)