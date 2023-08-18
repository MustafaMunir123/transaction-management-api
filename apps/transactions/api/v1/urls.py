from django.urls import path
from apps.transactions.api.v1.views import (
    AccountAPIView
)

urlpatterns = [
    path('account/create/', AccountAPIView.as_view())
]