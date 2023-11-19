import datetime
import pandas as pd
from rest_framework.views import APIView, status
from apps.utils import success_response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from apps.transactions.api.v1.serializers import (
    TransactionSerializer,
    AccountSerializer,
    CurrencySerializer
)
from apps.transactions.permissions import (
    OnlyAdmin,
    TransactionPermission
)
from apps.transactions.models import (
    Transaction,
    Currency,
)
from apps.transactions.api.v1.services import (
    ExportServices,
    LedgerServices,
    TransactionServices,
)
from apps.transactions.models import Account
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class AccountAPIView(APIView):
    permission_classes = [IsAuthenticated, OnlyAdmin]
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

    def get(self, request, pk=None):
        try:
            serializer = self.get_serializer()
            if pk:
                accounts = Account.objects.get(id=pk)
                serializer = serializer(accounts, many=False)
            else:
                accounts = Account.objects.all()
                serializer = serializer(accounts, many=True)
            return success_response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex


class TransactionsAPIView(PageNumberPagination, APIView):
    permission_classes = [IsAuthenticated, TransactionPermission]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get_serializer():
        return TransactionSerializer

    def post(self, request):
        try:
            complete_records = []
            for record in request.data["transactions"]:
                to_account = record.pop("to_account", None)
                from_account = record.pop("from_account", None)
                to_account_instance = Account.objects.get(id=to_account)
                from_account_instance = Account.objects.get(id=from_account)
                serializer = self.get_serializer()
                serializer = serializer(data=record)
                serializer.is_valid(raise_exception=True)
                serializer.save(
                    to_account=to_account_instance, from_account=from_account_instance
                )
                serializer.validated_data["to_account"] = to_account_instance.title
                serializer.validated_data["from_account"] = from_account_instance.title
                serializer.validated_data["entry_no"] = serializer.data["entry_no"]
                complete_records.append(serializer.validated_data)
            return success_response(
                data=complete_records, status=status.HTTP_200_OK
            )
        except Exception as ex:
            raise ex

    def get(self, request, pk=None):
        try:
            serializer = self.get_serializer()
            if pk:
                transaction = Transaction.objects.get(entry_no=pk, is_archived=False)
                serializer = serializer(transaction)
                response_data = serializer.data
            else:
                date = request.GET.get("date", None)
                today_date = datetime.datetime.today().date()
                if not date:
                    raise ValueError("Date not provided, must provide date param")
                queryset = Transaction.objects.filter(date__range=[date, today_date], is_archived=False).order_by('time')
                self.page_size = 100
                # paginated_data = self.paginate_queryset(queryset, request)
                serializer = serializer(queryset, many=True)
                list_of_dict = TransactionServices.denormalize_accounts(serialized_data=serializer.data)
                if not list_of_dict:
                    raise ValueError("No transactions.")
                dataframe = pd.DataFrame(list_of_dict)
                dataframe = TransactionServices.order_columns(dataframe=dataframe)
                data_dict = dataframe.to_dict('records')

                # "count": self.page.paginator.count,
                # "next": self.get_next_link(),
                # "previous": self.get_previous_link(),
                # "page_range": list(range(1, self.page.paginator.num_pages + 1))
                response_data = {
                    "results": data_dict,
                }
            return success_response(data=response_data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex

    def patch(self, request):
        transactions = request.data.get('transactions', [])
        try:
            entry_no = request.data.get("entry_no")
            is_valid = request.data.get("is_valid", True)
            if entry_no:
                print("pass")
                pk_list = TransactionServices.compile_pk_list(entry_no)
                transactions = Transaction.objects.filter(entry_no__in=pk_list)
                transactions.update(is_valid=is_valid)
                return success_response(data={"message": "updated successfully"}, status=status.HTTP_200_OK)
            for transaction in transactions:
                transaction_object = Transaction.objects.get(entry_no=transaction.pop("entry_no"))
                serializer = TransactionSerializer(transaction_object, data=transaction, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return success_response(data={"message": "updated successfully"}, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex


"""    
    def get(self, request, pk=None):
        try:
            serializer = self.get_serializer()
            if pk:
                user = Transaction.objects.get(entry_no=pk)
                serializer = serializer(user)
                response_data = serializer.data
            else:
                date = request.GET.get("date", None)
                today_date = datetime.datetime.today().date()
                if not date:
                    raise ValueError("Date not provided, must provide date param")
                queryset = Transaction.objects.filter(date__range=[date, today_date]).order_by('time')
                self.page_size = 100
                paginated_data = self.paginate_queryset(queryset, request)
                serializer = serializer(paginated_data, many=True)
                list_of_dict = TransactionServices.denormalize_accounts(serialized_data=serializer.data)
                dataframe = pd.DataFrame(list_of_dict)
                dataframe = ExportServices.order_columns(dataframe=dataframe)
                data_dict = dataframe.to_dict('records')

                response_data = {
                    "count": self.page.paginator.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "results": data_dict,
                    "page_range": list(range(1, self.page.paginator.num_pages + 1))
                }
            return success_response(data=response_data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex
"""


class ExportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def export_ledger(request, pk=None):
        try:
            data = LedgerAPIView().get(request=request, pk=pk).data
            ExportServices().export_ledger(data=data["data"])
            return success_response(data="File Created", status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex

    def get(self, request, pk=None):
        try:
            if "ledger" in request.path:
                return self.export_ledger(request=request, pk=pk)
            # else:
            #     return self.export_all(request)

        except Exception as ex:
            raise ex


class CurrencyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get_serializer():
        return CurrencySerializer

    def get(self, request):
        try:
            currencies = Currency.objects.all()
            serializer = self.get_serializer()
            serializer = serializer(currencies, many=True)
            return success_response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex


class LedgerAPIView(APIView):

    def get(self, request, pk: int):
        try:
            account = Account.objects.get(id=pk)
            account_serializer = AccountSerializer(account)
            transactions = Transaction.objects.filter(Q(from_account=pk) | Q(to_account=pk), is_valid=True,
                                                      is_archived=False).order_by("date").order_by("time")
            serializer = TransactionSerializer(transactions, many=True)
            debit_credit = LedgerServices.debit_credit(serializer.data, pk)
            LedgerServices.calculate_opening_closing(debit_credit=debit_credit)
            sorted_transactions = TransactionServices.sort_transactions(transactions=serializer.data)
            sorted_transactions = TransactionServices.denormalize_accounts(sorted_transactions)
            restructured_data = LedgerServices.restructure_data(data_list=sorted_transactions, pk=pk,
                                                                debit_credit=debit_credit)
            data = {
                "account": account_serializer.data,
                "debit_credit": debit_credit,
                "transactions": restructured_data
            }
            # if request.data["export"]:
            #     LedgerServices.create_update_opening(debit_credit, pk)
            return success_response(data=data, status=status.HTTP_200_OK)

        except Exception as ex:
            raise ex


class TransactionNumber(APIView):

    def get(self, request):
        try:
            last_object = Transaction.objects.last()
            if last_object:
                return success_response(data={"entry_no": last_object.entry_no}, status=status.HTTP_200_OK)
            return success_response(data={"entry_no": 0}, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex


class SummaryAPIView(APIView):

    @staticmethod
    def export_all(pk_list):
        try:
            transactions = Transaction.objects.filter(Q(from_account__in=pk_list) | Q(to_account__in=pk_list),
                                                      is_valid=True, is_archived=False).order_by("date").order_by("time")
            serializer = TransactionSerializer(transactions, many=True)
            list_of_dict = TransactionServices.denormalize_accounts(serialized_data=serializer.data)
            ExportServices().export_all(serialized_data=list_of_dict)

            return success_response(data={"message": "File Generated"}, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex

    def get(self, request):
        try:
            data_list = []
            pk_list = []
            export = request.data.get("export")
            accounts = Account.objects.filter()
            account_serializer = AccountSerializer(accounts, many=True)
            for account in account_serializer.data:
                pk = account["id"]
                data = LedgerAPIView().get(request=request, pk=pk).data
                data["data"].pop("transactions")
                if export:
                    LedgerServices.create_update_opening(data["data"]["debit_credit"], pk)
                pk_list.append(pk)
                data_list.append(data["data"])
            if export:
                print("che")
                self.export_all(pk_list)
                transactions = Transaction.objects.filter(Q(from_account__in=pk_list) | Q(to_account__in=pk_list), is_valid=True,
                                                          is_archived=False).order_by("date").order_by("time")
                transactions.update(is_archived=True)
            return success_response(data=data_list, status=status.HTTP_200_OK)
        except Exception as ex:
            raise ex