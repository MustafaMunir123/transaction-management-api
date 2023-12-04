# Standard Library Imports
import copy
import json
import os
from datetime import datetime
from operator import itemgetter
from typing import Dict, List, OrderedDict

# Third Party Imports
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows

# Local Imports
# from apps.transactions.api.v1.serializers import CurrencyOpeningSerializer
from apps.transactions.constants import EXPORT_ALL, EXPORT_LEDGER
from apps.transactions.models import Account, CurrencyOpening, Transaction


class ExportServices:
    download_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

    def export_all(self, serialized_data: List[Dict]) -> None:
        if not serialized_data:
            raise ValueError("No new transactions made.")
        df = pd.DataFrame(serialized_data)
        print(df.columns)
        df.drop(columns=["is_archived", "is_valid"])
        df = self.order_columns(dataframe=df)
        edited_columns = []
        for column in df.columns:
            if column in EXPORT_ALL.keys():
                edited_columns.append(EXPORT_ALL[column])
            else:
                edited_columns.append(column)
        df.columns = edited_columns

        """
        Generating .xlsx with custom formatting
        """
        workbook = Workbook()
        worksheet = workbook.active
        for row in dataframe_to_rows(df, index=False, header=True):
            worksheet.append(row)
        for cell in worksheet[1]:
            cell.font = Font(bold=True)
        workbook.save(f"{self.download_path}/transactions.xlsx")

    @staticmethod
    def order_columns(dataframe):
        column_order = [
            "entry_no",
            "from_account_id",
            "from_account_title",
            "initial_amount",
            "from_currency",
            "multiply_by",
            "divide_by",
            "converted_amount",
            "to_currency",
            "to_account_id",
            "to_account_title",
            "narration",
            "date",
        ]
        return dataframe[column_order]

    @staticmethod
    def order_ledger_columns(dataframe):
        column_order = ["entry_no", "date", "narration", "currency", "debit_amount", "credit_amount", "balance"]
        return dataframe[column_order]

    def export_ledger(self, data, account) -> None:
        transactions_dataframe = pd.DataFrame(data["transactions"])
        transactions_dataframe.pop("title")
        transactions_dataframe = self.order_ledger_columns(transactions_dataframe)
        edited_columns = []
        for column in transactions_dataframe.columns:
            if column in EXPORT_LEDGER.keys():
                edited_columns.append(EXPORT_LEDGER[column])
            else:
                edited_columns.append(column)
        transactions_dataframe.columns = edited_columns
        general_info = {
            "title": data["account"].pop("title"),
            "date": datetime.today().date(),
            "time": datetime.today().time(),
        }
        general_dataframe = pd.DataFrame(general_info, index=[1])
        general_dataframe.columns = general_dataframe.columns.str.upper()

        """
        Generating .xlsx with custom formatting
        """
        workbook = Workbook()
        worksheet = workbook.active

        row_number = self.append_to_worksheet(worksheet, general_dataframe, 1)
        self.append_to_worksheet(worksheet, transactions_dataframe, row_number)

        workbook.save(f"{self.download_path}/{account.title}.xlsx")

    @staticmethod
    def append_to_worksheet(worksheet, dataframe, row_number, index=False):
        header = row_number
        for row in dataframe_to_rows(dataframe, index=index, header=True):
            row_number += 1
            worksheet.append(row)
        worksheet.append([])
        row_number += 1
        for cell in worksheet[header]:
            cell.font = Font(bold=True)
        return row_number


class TransactionServices:
    @staticmethod
    def sort_transactions(transactions: List) -> List:
        transactions.sort(key=itemgetter("entry_no"))
        return transactions

    @staticmethod
    def order_columns(dataframe):
        column_order = [
            "entry_no",
            "from_account_id",
            "from_account_title",
            "initial_amount",
            "from_currency",
            "multiply_by",
            "divide_by",
            "converted_amount",
            "to_currency",
            "to_account_id",
            "to_account_title",
            "narration",
            "is_valid",
            "date",
        ]
        return dataframe[column_order]

    @staticmethod
    def denormalize_accounts(serialized_data: List[OrderedDict]) -> List:
        list_of_dict = json.loads(json.dumps(serialized_data))
        for data in list_of_dict:
            from_data = data.pop("from_account")
            to_data = data.pop("to_account")

            data["from_account_id"] = from_data["id"]
            data["from_account_title"] = from_data["title"]
            data["to_account_id"] = to_data["id"]
            data["to_account_title"] = to_data["title"]
        return list_of_dict

    @staticmethod
    def compile_pk_list(entry_no: int) -> List:
        last_object = Transaction.objects.last()
        last_entry_no = last_object.entry_no
        pk_list = []

        for number in range(entry_no, last_entry_no + 1):
            pk_list.append(number)
        return pk_list


class LedgerServices:
    @staticmethod
    def debit_credit(transactions: List, pk: int) -> Dict:
        currency_records = {}
        for transaction in transactions:
            if transaction["from_account"]["id"] == pk:
                if transaction["from_currency"] in currency_records.keys():
                    currency_records[transaction["from_currency"]]["debit"] += transaction["initial_amount"]
                else:
                    currency_records[transaction["from_currency"]] = {"debit": 0, "credit": 0}
                    currency_records[transaction["from_currency"]]["debit"] += transaction["initial_amount"]
            else:
                if transaction["to_currency"] in currency_records.keys():
                    currency_records[transaction["to_currency"]]["credit"] += transaction["converted_amount"]
                else:
                    currency_records[transaction["to_currency"]] = {"debit": 0, "credit": 0}
                    currency_records[transaction["to_currency"]]["credit"] += transaction["converted_amount"]
        return currency_records

    @staticmethod
    def calculate_opening_closing(debit_credit: Dict, pk) -> None:
        for key, value in debit_credit.items():
            debit_credit[key]["closing"] = debit_credit[key]["debit"] - debit_credit[key]["credit"]
            if CurrencyOpening.objects.filter(currency=key, account=pk).exists():
                obj = CurrencyOpening.objects.get(currency=key, account=pk)
                debit_credit[key]["opening"] = obj.opening
            else:
                debit_credit[key]["opening"] = 0

    @staticmethod
    def restructure_data(data_list: List, pk: int, debit_credit: Dict) -> List:
        records = []

        duplicate_dict = copy.deepcopy(debit_credit)
        for data in data_list:
            record = {
                "entry_no": data["entry_no"],
                "date": data["date"],
                "title": "",
                "currency": "",
                "debit_amount": 0,
                "credit_amount": 0,
                "narration": data["narration"],
                "balance": 0,
            }
            if data["from_account_id"] == pk:
                record["debit_amount"] = data["initial_amount"]
                record["currency"] = data["from_currency"]
                record["title"] = data["to_account_title"]
                duplicate_dict[record["currency"]]["opening"] += record["debit_amount"]
                record["balance"] = duplicate_dict[record["currency"]]["opening"]
            else:
                record["credit_amount"] = data["converted_amount"]
                record["currency"] = data["to_currency"]
                record["title"] = data["from_account_title"]
                duplicate_dict[record["currency"]]["opening"] -= record["credit_amount"]
                record["balance"] = duplicate_dict[record["currency"]]["opening"]

            records.append(record)
        return records

    @staticmethod
    def create_update_opening(opening_closing: Dict, pk: int) -> None:
        for currency in opening_closing.keys():
            if CurrencyOpening.objects.filter(currency=currency, account=pk).exists():
                obj = CurrencyOpening.objects.get(currency=currency, account=pk)
                obj.opening = opening_closing[currency]["closing"]
                obj.save()
            else:
                account = Account.objects.get(id=pk)
                obj = CurrencyOpening.objects.create(
                    currency=currency, account=account, opening=opening_closing[currency]["closing"]
                )
                obj.save()


# class SummaryServices:
