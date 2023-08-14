from django.urls import path, include
from apps.users.api import urls as USERS_API

urlpatterns = [
    path('users/', include(USERS_API))
]
