from django.urls import path
from apps.users.api.v1.views import (
    LoginUserDetailView
)

urlpatterns = [
    path('login/', LoginUserDetailView.as_view())
]
