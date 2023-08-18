from django.urls import path, include
from apps.users.api import urls as USERS_API
from apps.transactions.api import urls as TRANSACTION_API

urlpatterns = [
    path('users/', include(USERS_API)),
    path('transactions/', include(TRANSACTION_API))
]
