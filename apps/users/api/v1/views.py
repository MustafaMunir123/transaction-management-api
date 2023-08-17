from django.contrib.auth import authenticate
from rest_framework.views import APIView, Response, status
from apps.users.api.v1.serializers import (
    LoginSerializer,
    CustomUserSerializer,
    RegisterSerializer
)
from apps.users.functions import (
    get_token_for_user,
    create_token_for_user
)
# Create your views here.


class LoginDetailsAPIView(APIView):

    @staticmethod
    def get_login_serializer():
        return LoginSerializer

    @staticmethod
    def get_serializer():
        return CustomUserSerializer

    def post(self, request):
        try:
            serializer = self.get_login_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if not user:
                raise ValueError(
                    "Unable to log in with provided credentials."
                )
            serializer = self.get_serializer()
            serializer = serializer(user)
            token = get_token_for_user(user)
            context = {
                "success": True,
                "data": {"token": token, "user": serializer.data},
            }

            return Response(context)
        except Exception as err:
            raise err

class RegisterUserAPIView(APIView):

    @staticmethod
    def get_serializer():
        return RegisterSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = create_token_for_user(serializer.validated_data["email"])
            serializer.validated_data.update({
                "token": token
            })
            return Response(serializer.validated_data)
        except Exception as ex:
            raise ex