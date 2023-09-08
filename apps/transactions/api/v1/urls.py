from django.urls import path
from apps.transactions.api.v1.views import (
    AccountAPIView,
    TransactionsAPIView,
    ExportAPIView
)

urlpatterns = [
    path("account/create/", AccountAPIView.as_view()),
    path("create/", TransactionsAPIView.as_view()),
    path("all/details/", TransactionsAPIView.as_view()),
    path("<int:pk>/details/", TransactionsAPIView.as_view()),
    path("export/all/", ExportAPIView.as_view())
]
