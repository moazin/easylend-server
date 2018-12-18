from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import json

from transactions.serializers import TransactionReadSerializer, TransactionCreateSerializer, ExchangeSerializer, TransactionVerificationSerializer
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

    # TODO: Do this with object_permission maybe! This is a crude way I think
    def initial(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.data['from_user'] != self.request.user.id:
                self.permission_denied(request, message=getattr(IsAuthenticated, 'message', None))
        return super().initial(request, *args, **kwargs)

class MyTransactionsWithEveryone(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionReadSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'GET':
            user = self.request.user
            return Transaction.objects.filter(Q(from_user=user) | Q(to_user=user)).order_by('-date')
        else:
            return super().get_queryset()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myExchangeWithEveryoneView(request):
    if request.method == 'GET':
        results = User.objects.raw("select auth_user.id, auth_user.first_name, auth_user.last_name, auth_user.username, ((select coalesce((select sum(amount) from transactions_transaction WHERE from_user_id=%s AND to_user_id=auth_user.id GROUP BY to_user_id), 0)) - (select coalesce((select sum(amount) from transactions_transaction WHERE from_user_id=auth_user.id AND to_user_id=%s GROUP BY to_user_id), 0))) AS exchange from auth_user where auth_user.id <> %s", [request.user.id, request.user.id, request.user.id])
        exchanges = ExchangeSerializer(results, many=True)        
        return Response(exchanges.data)

class MyTransactionsWithSomeone(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionReadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'GET':
            user = self.request.user
            other_guy = get_object_or_404(User, id=self.request.GET.get('id'))
            return Transaction.objects.filter(Q(from_user=user, to_user=other_guy) | Q(to_user=user, from_user=other_guy)).order_by('-date')
        else:
            return super().get_queryset()

class VerifyTransaction(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionVerificationSerializer
    permission_classes = (IsAuthenticated,)

    def check_object_permissions(self, request, obj):
        if request.user.id != obj.to_user.id:
            self.permission_denied(request, message=getattr(IsAuthenticated, 'message', None))
        return super().check_object_permissions(request, obj)

    def partial_update(self, request, *args, **kwargs):
        request.data.update({
            "verified": True
        })
        return super().partial_update(request, *args, **kwargs)

class UnVerifiedTransactions(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionReadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(to_user=self.request.user, verified=False)