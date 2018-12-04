from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import json

from transactions.serializers import TransactionReadSerializer, TransactionCreateSerializer, ExchangeSerializer
from transactions.models import Transaction

class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionReadSerializer
    serializer_class_write = TransactionCreateSerializer

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            if hasattr(self, 'serializer_class_write'):
                return self.serializer_class_write
        else:
            return super().get_serializer_class()

class TransactionSearchView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionReadSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'GET':
            user = self.request.user
            return Transaction.objects.filter(Q(from_user=user) | Q(to_user=user))
        else:
            return super().get_queryset()

@api_view(['GET'])
def myExchangeWithEveryoneView(request):
    if request.method == 'GET':
        results = User.objects.raw("select auth_user.id, auth_user.username, ((select sum(amount) from transactions_transaction WHERE from_user_id=%s AND to_user_id=auth_user.id GROUP BY to_user_id)-(select sum(amount) from transactions_transaction WHERE from_user_id=auth_user.id AND to_user_id=%s GROUP BY to_user_id)) AS exchange from auth_user where auth_user.id <> %s", [request.user.id, request.user.id, request.user.id])
        exchanges = ExchangeSerializer(results, many=True)        
        return Response(exchanges.data)