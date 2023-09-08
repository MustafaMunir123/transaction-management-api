import pandas as pd
from typing import Dict


class ExportServices:
    @staticmethod
    def export_all(serialized_data: Dict) -> None:
        df = pd.DataFrame(serialized_data)
        df.to_csv("./templates/transactions/test.csv")
