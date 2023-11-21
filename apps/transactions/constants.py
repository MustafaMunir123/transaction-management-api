from apps.transactions.enums import CurrencyEnum

CURRENCY_CHOICES = (
    (CurrencyEnum.MZN.name, CurrencyEnum.MZN.value),
    (CurrencyEnum.USD.name, CurrencyEnum.USD.value),
    (CurrencyEnum.ZAR.name, CurrencyEnum.ZAR.value),
    (CurrencyEnum.AED.name, CurrencyEnum.AED.value),
    (CurrencyEnum.EUR.name, CurrencyEnum.EUR.value),
)

EXPORT_ALL = {
    "entry_no": "ENTRY NO.",
    "multiply_by": "MULTIPLY",
    "divide_by": "DIVIDE",
    "from_account_title": "ACCOUNT 1",
    "from_account_id": "ACCOUNT #1 ID",
    "to_account_title": "ACCOUNT 2",
    "to_account_id": "ACCOUNT #2 ID",
    "date": "DATE",
    "from_currency": "FROM CURRENCY",
    "to_currency": "TO CURRENCY",
    "initial_amount": "INITIAL AMOUNT",
    "converted_amount": "CONVERTED AMOUNT",
    "narration": "NARRATION"
}

EXPORT_LEDGER = {
    "entry_no": "V.R. #",
    "date": "DATE",
    "title": "TITLE",
    "currency": "CURRENCY",
    "debit_amount": "DEBIT AMOUNT",
    "credit_amount": "CREDIT AMOUNT",
    "narration": "NARRATION",
    "balance": "BALANCE"
}
