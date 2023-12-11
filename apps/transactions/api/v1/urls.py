# Third Party Imports
# from django.conf.urls import include
from django.urls import path

# Local Imports
from apps.transactions.api.v1.views import (
    AccountAPIView,
    CurrencyAPIView,
    ExportAPIView,
    LedgerAPIView,
    SummaryAPIView,
    TransactionNumber,
    TransactionsAPIView,
)

urlpatterns = [
    path("account/create/", AccountAPIView.as_view()),
    path("account/<int:pk>/", AccountAPIView.as_view()),
    path("account/all/", AccountAPIView.as_view()),
    path("create/", TransactionsAPIView.as_view()),
    path("update/", TransactionsAPIView.as_view()),
    path("all/details/", TransactionsAPIView.as_view()),
    path("<int:pk>/details/", TransactionsAPIView.as_view()),
    path("export/all/", ExportAPIView.as_view()),
    path("export/<int:pk>/ledger/", ExportAPIView.as_view()),
    path("currency/all/", CurrencyAPIView.as_view()),
    path("<int:pk>/ledger/", LedgerAPIView.as_view()),
    path("entry-no/", TransactionNumber.as_view()),
    path("summary/", SummaryAPIView.as_view()),
]
