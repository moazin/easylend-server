from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from . import serializers

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfileView(request):
    user_obj = serializers.UserSerializer(request.user)
    return Response(user_obj.data)