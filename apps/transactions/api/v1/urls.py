from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.transactions.api.v1.views import (
    AccountAPIView,
    TransactionsAPIView,
    CurrencyAPIView,
    ExportAPIView,
    LedgerAPIView,
    TransactionNumber
)
router = DefaultRouter()

# router.register("", TransactionsAPIView, basename='Transaction')

urlpatterns = [
    path("account/create/", AccountAPIView.as_view()),
    path("account/<int:pk>/", AccountAPIView.as_view()),
    path("account/all/", AccountAPIView.as_view()),
    url("", include(router.urls)),
    path("create/", TransactionsAPIView.as_view()),
    path("update/", TransactionsAPIView.as_view()),
    path("all/details/", TransactionsAPIView.as_view()),
    path("<int:pk>/details/", TransactionsAPIView.as_view()),
    path("export/all/", ExportAPIView.as_view()),
    path("export/<int:pk>/ledger/", ExportAPIView.as_view()),
    path('currency/all/', CurrencyAPIView.as_view()),
    path('<int:pk>/ledger/', LedgerAPIView.as_view()),
    path('entry-no/', TransactionNumber.as_view())
]
