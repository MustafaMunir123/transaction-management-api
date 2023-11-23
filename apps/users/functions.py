# Third Party Imports
from rest_framework.authtoken.models import Token

# Local Imports
from apps.users.models import CustomUser


def get_token_for_user(user: CustomUser) -> str:
    token = Token.objects.get(user=user)
    return token.key


def create_token_for_user(email: str) -> str:
    user = CustomUser.objects.get(email=email)
    token = Token.objects.create(user=user)
    return token.key
