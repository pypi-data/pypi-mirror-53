import re

import numpy
import pandas as pd
import tabula

from .base import AllergenState, BaseParser
from .util import removeNewLine

REMOTE_URL = "http://www3.akindo-sushiro.co.jp/pdf/menu/allergy.pdf"
BASE_LAYOUT = [
    ("卵", "egg", True),  # header, key, required
    ("乳", "milk", True),
    ("小麦", "wheat", True),
    ("えび", "shrimp", True),
    ("かに", "crab", True),
    ("そば", "buckwheat", True),
    ("落花生", "peanut", True),
    ("あわび", "abalone", True),
    ("いか", "squid", True),
    ("いくら", "salmonRoe", True),
    ("オレンジ", "orange", True),
    ("キウイ", "kiwi", True),
    ("牛肉", "beef", True),
    ("クルミ", "walnut", True),
    ("鮭", "salmon", True),
    ("さば", "mackerel", True),
    ("大豆", "soybean", True),
    ("鶏肉", "chicken", True),
    ("バナナ", "banana", True),
    ("豚肉", "pork", True),
    ("松茸", "matsutakeMushroom", True),
    ("桃", "peach", True),
    ("山芋", "yamOrSweetPotato", True),
    ("りんご", "apple", True),
    ("ゼラチン", "gelatin", True),
    ("ごま", "sesame", True),
    ("カシューナッツ", "cashewNut", True),
]
TABLE_LAYOUT = [
    ("分類", "category", True),
    ("商品名", "name", True),
    *BASE_LAYOUT,
    ("なし", "none", False),
]


class SushiroAllergyParser(BaseParser):
    def parse(self, filename: str = REMOTE_URL) -> pd.DataFrame:
        df = self._parse_table(filename, TABLE_LAYOUT)

        for _, key, _ in BASE_LAYOUT:
            df[key] = df[key].map(self.allergen_state_of)

        return df

    def _parse_table(self, filename, layout) -> pd.DataFrame:

        df = tabula.read_pdf(filename, pages="all", lattice=True)

        columns = [re.sub(r"\s", "", column) for column in df.columns]
        expected_columns = [column[0] for column in layout]
        assert columns == expected_columns, f"{filename} のテーブルレイアウトが変更されました。"

        df.columns = [column[1] for column in layout]

        # Remove unnecessary columns
        for _, key, required in layout:
            if not required:
                del df[key]

        df_filterd = df.query('category != "分類"')

        df_cleansed = df_filterd.applymap(removeNewLine)

        return df_cleansed

    def allergen_state_of(self, value: str) -> AllergenState:
        if value == "●":
            return AllergenState.CONTAIN
        elif value == "○":
            return AllergenState.MAY_CONTAIN
        elif numpy.isnan(value):
            return AllergenState.NOT_CONTAIN
        else:
            raise ValueError(f"Unknown AllergenState {value}.")

