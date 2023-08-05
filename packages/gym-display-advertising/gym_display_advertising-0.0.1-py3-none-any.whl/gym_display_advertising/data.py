from pathlib import Path
from typing import List

import pandas as pd


class ProcessedIPinYouData:
    def __init__(self, directory: Path, columns: List = ["click", "winprice"]):
        self.directory = directory
        self.columns = columns

    def get_merchant_data(self, merchant_id: int):
        mechant_dir = self.directory / str(merchant_id)
        train_data = pd.read_csv(
            mechant_dir / "train.yzx.txt",
            header=None,
            index_col=False,
            sep=" ",
            names=self.columns,
            usecols=self.columns,
        )
        test_data = pd.read_csv(
            mechant_dir / "test.yzx.txt",
            header=None,
            index_col=False,
            sep=" ",
            names=self.columns,
            usecols=self.columns,
        )
        return train_data, test_data
