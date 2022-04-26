from django.core.exceptions import PermissionDenied
from rest_framework import viewsets

from cats.models import Achievement, Cat, User

from cats.serializers import (
    AchievementSerializer, CatSerializer, UserSerializer
)


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    # Не доделано. Этим методом текеущий юзер может присвоить себе чужого кота
    # def perform_update(self, serializer):
    #     serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied('Изменять параметры чужого котика нельзя!')
        super(CatViewSet, self).perform_update(serializer) 


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
