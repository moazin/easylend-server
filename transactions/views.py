from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from transactions.serializers import TransactionReadSerializer, TransactionCreateSerializer
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