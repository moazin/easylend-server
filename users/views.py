from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from . import serializers

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfileView(request):
    user_obj = serializers.UserSerializer(request.user)
    return Response(user_obj.data)

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username
        })