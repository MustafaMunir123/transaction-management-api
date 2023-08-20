from rest_framework.views import APIView, status
from apps.utils import success_response
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from apps.transactions.api.v1.serializers import (
    TransactionSerializer,
    AccountSerializer,
)
from apps.transactions.models import (
    Transaction
)
from apps.transactions.models import Account
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.


class AccountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get_serializer():
        return AccountSerializer

    def post(self, request):
        try:
            user = request.user
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return success_response(
                data=serializer.validated_data, status=status.HTTP_200_OK
            )
        except Exception as ex:
            raise ex


class TransactionsAPIView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get_serializer():
        return TransactionSerializer

    def post(self, request):
        try:
            to_account = request.data.pop("to_account", None)
            from_account = request.data.pop("from_account", None)
            to_account_instance = Account.objects.get(id=to_account)
            from_account_instance = Account.objects.get(id=from_account)
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                to_account=to_account_instance, from_account=from_account_instance
            )
            serializer.validated_data["to_account"] = to_account_instance.title
            serializer.validated_data["from_account"] = from_account_instance.title
            serializer.validated_data["entry_no"] = serializer.data["entry_no"]
            return success_response(
                data=serializer.validated_data, status=status.HTTP_200_OK
            )
        except Exception as ex:
            raise ex

    def get(self, request, pk=None):
        try:
            serializer = self.get_serializer()
            if pk:
                user = Transaction.objects.get(id=pk)
                serializer = serializer(user)
                response_data = serializer.data
            else:
                queryset = Transaction.objects.filter(date=datetime.today().date()).order_by('time').values()
                self.page_size = 2
                paginated_data = self.paginate_queryset(queryset, request)
                serializer = serializer(paginated_data, many=True)
                response_data = {
                    "count": self.page.paginator.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "results": serializer.data,
                    "page_range": list(range(1, self.page.paginator.num_pages + 1))
                }
            return success_response(data=response_data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex
