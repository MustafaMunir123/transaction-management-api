from django.urls import (
    path
)
from apps.users.api.v1.views import (
    LoginDetailsAPIView,
    RegisterUserAPIView,
    UserAPIView
)

urlpatterns = [
    path('login/', LoginDetailsAPIView.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('all/details/', UserAPIView.as_view()),
    path('<int:pk>/details/', UserAPIView.as_view())
]
