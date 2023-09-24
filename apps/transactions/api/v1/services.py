from typing import Dict, List

import pandas as pd
from operator import itemgetter


class ExportServices:

    @staticmethod
    def export_all(serialized_data: Dict) -> None:
        df = pd.DataFrame(serialized_data)
        df.to_csv("./templates/transactions/test.csv")


class TransactionServices:

    @staticmethod
    def sort_transactions(transactions: List) -> List:
        transactions.sort(key=itemgetter("entry_no"))
        return transactions


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


