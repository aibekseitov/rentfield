from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny, IsAdminUser, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Auth.models import User, Profile
from Auth.serializers import UserReadSerializer, UserWriteSerializer, ProfileUpdateSerializer, ProfileReadSerializer


class UserViewSet(ModelViewSet):
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
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self, *args, **kwargs):
        """
        Если тип запроса GET, HEAD, OPTIONS, то изменяет serializer
        """
        if self.request.method in SAFE_METHODS:
            return UserReadSerializer
        return UserWriteSerializer

    @list_route(methods=["get"], permission_classes=[IsAuthenticated])
    def get_token(self,request):
        try:
            token = Profile.objects.get(user=request.user).token
            return Response(status=status.HTTP_200_OK, data={'token': token})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={})

    @list_route(methods=["get"], permission_classes=[IsAuthenticated])
    def get_profile(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            profile_serializer = ProfileReadSerializer(instance=profile)
            return Response(status=status.HTTP_200_OK, data=profile_serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={})

    @list_route(methods=["post"], permission_classes=[IsAuthenticated])
    def update_password(self, request):
        try:
            user = request.user
            user.set_password(request.data['password'])
            user.save()
            return Response(status=status.HTTP_200_OK, data={'message' : 'Password successfully changed.'})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message' : 'The password field is required.'})

    @list_route(methods=["post"], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        try:
            user = request.user
            profile = Profile.objects.get(user=user)
            serializer = ProfileUpdateSerializer(data=request.data)
            serializer.is_valid()
            serializer.update(profile, serializer.validated_data)
            return Response(status=status.HTTP_200_OK, data=serializer.validated_data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Something is wrong.'})