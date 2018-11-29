from django.shortcuts import render
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