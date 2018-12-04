from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransactionListCreateView.as_view()),
    path('mytransactionswitheveryone', views.MyTransactionsWithEveryone.as_view()),
    path('myexchangewitheveryone', views.myExchangeWithEveryoneView),
    path('mytransactionswithsomeone', views.MyTransactionsWithSomeone.as_view())
]