# Third Party Imports
from django.urls import include, path

# Local Imports
from apps.transactions.api import urls as TRANSACTION_API
from apps.users.api import urls as USERS_API

urlpatterns = [
    path("users/", include(USERS_API)),
    path("transactions/", include(TRANSACTION_API)),
]
