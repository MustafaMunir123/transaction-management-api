# Third Party Imports
from django.urls import include, path

# Local Imports
from apps.users.api.v1 import urls as V1_USERS

urlpatterns = [
    path("v1/", include(V1_USERS)),
]
