from django.urls import (
    path,
    include
)
from apps.users.api.v1.views import (
    LoginDetailsAPIView,
RegisterUserAPIView
)

urlpatterns = [
    path('login/', LoginDetailsAPIView.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
]
