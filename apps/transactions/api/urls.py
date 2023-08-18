from django.urls import (
    path,
    include
)
from apps.transactions.api.v1 import urls as V1_TRANSACTION

urlpatterns = [
    path('v1/', include(V1_TRANSACTION))
]