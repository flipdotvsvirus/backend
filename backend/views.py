from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

from backend.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
