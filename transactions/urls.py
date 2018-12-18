from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.TransactionListCreateView.as_view()),
    path('mytransactionswitheveryone', views.MyTransactionsWithEveryone.as_view()),
    path('myexchangewitheveryone', views.myExchangeWithEveryoneView),
    path('mytransactionswithsomeone', views.MyTransactionsWithSomeone.as_view()),
    path(r'verifytransaction/<int:pk>/', views.VerifyTransaction.as_view()),
    path('unverifiedtransactions', views.UnVerifiedTransactions.as_view())
]