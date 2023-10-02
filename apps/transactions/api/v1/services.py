import json
import pandas as pd
from typing import Dict, List, OrderedDict
from operator import itemgetter
from apps.transactions.constants import EXPORT_ALL
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font


class ExportServices:

    def export_all(self, serialized_data: List[Dict]) -> None:
        df = pd.DataFrame(serialized_data)
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
        workbook.save("./templates/transactions/test.xlsx")
        # df.to_csv("./templates/transactions/test.csv")

    @staticmethod
    def order_columns(dataframe):
        column_order = ['entry_no', 'from_account_id', 'from_account_title', 'initial_amount', 'from_currency', 'multiply_by', 'divide_by', 'converted_amount', 'to_currency', 'to_account_id', 'to_account_title', 'narration']
        return dataframe[column_order]


class TransactionServices:

    @staticmethod
    def sort_transactions(transactions: List) -> List:
        transactions.sort(key=itemgetter("entry_no"))
        return transactions

    @staticmethod
    def denormalize_accounts(serialized_data: OrderedDict) -> List:
        list_of_dict = json.loads(json.dumps(serialized_data))
        for data in list_of_dict:
            from_data = data.pop("from_account")
            to_data = data.pop("to_account")

            data["from_account_id"] = from_data["id"]
            data["from_account_title"] = from_data["title"]
            data["to_account_id"] = to_data["id"]
            data["to_account_title"] = to_data["title"]
        return list_of_dict


class LedgerServices:

    @staticmethod
    def debit_credit(from_transactions: List, to_transactions: List) -> Dict:
        currency_records = {}

        for transaction in from_transactions:
            if transaction["from_currency"] not in currency_records.keys():
                currency_records[transaction["from_currency"]] = {"debit": 0, "credit": 0}
            currency_records[transaction["from_currency"]]["debit"] += transaction["initial_amount"]

        for transaction in to_transactions:
            if transaction["to_currency"] not in currency_records.keys():
                currency_records[transaction["to_currency"]] = {"debit": 0, "credit": 0}
            currency_records[transaction["to_currency"]]["credit"] += transaction["converted_amount"]
        return currency_records

    @staticmethod
    def calculate_opening_closing(debit_credit: Dict) -> None:
        for key, value in debit_credit.items():
            debit_credit[key]["closing"] = debit_credit[key]["debit"] - debit_credit[key]["credit"]
