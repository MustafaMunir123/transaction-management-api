# Third Party Imports
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Response, status

# Local Imports
from apps.transactions.api.v1.urls import router
from apps.users.api.permissions import IsAuthenticatedAndAdmin
from apps.users.api.v1.serializers import CustomUserSerializer, LoginSerializer, RegisterSerializer
from apps.users.functions import create_token_for_user, get_token_for_user
from apps.users.models import CustomUser
from apps.utils import success_response

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
                raise ValueError("Unable to log in with provided credentials.")
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
            serializer.validated_data.update({"token": token})
            return Response(serializer.validated_data)
        except Exception as ex:
            raise ex


class UserAPIView(APIView):
    permission_classes = [IsAuthenticatedAndAdmin]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get_serializer():
        return CustomUserSerializer

    def get(self, request, pk=None):
        try:
            print(router.urls)
            serializer = self.get_serializer()
            if pk:
                user = CustomUser.objects.get(id=pk)
                serializer = serializer(user)
            else:
                queryset = CustomUser.objects.all()
                serializer = serializer(queryset, many=True)
            return success_response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex
