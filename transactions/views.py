from django.shortcuts import render
from rest_framework import generics

from transactions.serializers import TransactionReadSerializer, TransactionCreateSerializer
from transactions.models import Transaction

class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionReadSerializer
    serializer_class_write = TransactionCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            if hasattr(self, 'serializer_class_write'):
                return self.serializer_class_write
        else:
            return super().get_serializer_class()