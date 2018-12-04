from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransactionListCreateView.as_view()),
    path('mytransactions', views.TransactionSearchView.as_view())
]