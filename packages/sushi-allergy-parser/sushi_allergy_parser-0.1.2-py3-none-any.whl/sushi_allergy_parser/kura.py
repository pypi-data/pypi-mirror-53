import re

import numpy
import pandas as pd
import tabula

from .base import AllergenState, BaseParser
from .util import removeNewLine

REMOTE_URL = "http://www.kura-corpo.co.jp/common/pdf/kura_allergen.pdf"
BASE_LAYOUT = [
    ("卵", "egg", True),  # header, key, required
    ("小麦", "wheat", True),
    ("乳・乳製品", "milk", True),
    ("落花生ピーナッツ", "peanut", True),
    ("ソバ", "buckwheat", True),
    ("えび", "shrimp", True),
    ("かに", "crab", True),
    ("いか", "squid", True),
    ("いくら", "salmonRoe", True),
    ("さけ", "salmon", True),
    ("さば", "mackerel", True),
    ("牛肉", "beef", True),
    ("鶏肉", "chicken", True),
    ("豚肉", "pork", True),
    ("大豆", "soybean", True),
    ("オレンジ", "orange", True),
    ("りんご", "apple", True),
    ("ゼラチン", "gelatin", True),
    ("クルミ", "walnut", True),
    ("バナナ", "banana", True),
    ("キウイ", "kiwi", True),
    ("山芋", "yamOrSweetPotato", True),
    ("モモ", "peach", True),
    ("ごま", "sesame", True),
    ("あわび", "abalone", True),
    ("カシューナッツ", "cashewNut", True),
    ("松茸", "matsutakeMushroom", True),
]
PAGE1_LAYOUT = [
    ("品名", "name", True),
    ("(kカ一cロ皿aリ当lーり)", "calory", False),
    ("該当なし", "none", False),
    *BASE_LAYOUT,
]
PAGE2_LAYOUT = PAGE1_LAYOUT
PAGE3_LAYOUT = [
    ("品名", "name", True),
    ("一(皿kカ・cロ一aリlー杯当)り", "calory", False),
    ("該当なし", "none", False),
    *BASE_LAYOUT,
]
PAGE4_LAYOUT = [("品名", "name", True), ("該当なし", "none", False), *BASE_LAYOUT]
PAGES = [
    ("1", "定番寿司", PAGE1_LAYOUT),
    ("2", "限定商品", PAGE2_LAYOUT),
    ("3", "サイドメニュー", PAGE3_LAYOUT),
    ("4", "その他", PAGE4_LAYOUT),
]


class KuraAllergyParser(BaseParser):
    def parse(self, filename: str = REMOTE_URL) -> pd.DataFrame:
        df_list = []
        for page, category, layout in PAGES:
            df = self._parse_table(filename, page, category, layout)
            df_list.append(df)

        df_all = pd.concat(df_list, ignore_index=True)

        for _, key, _ in BASE_LAYOUT:
            df_all[key] = df_all[key].map(self.allergen_state_of)

        return df_all

    def _parse_table(
        self, filename: str, page: int, category: str, layout: list
    ) -> pd.DataFrame:

        df = tabula.read_pdf(filename, pages=str(page), lattice=True)

        columns = [re.sub(r"\s", "", column) for column in df.columns]
        expected_columns = [column[0] for column in layout]
        assert columns == expected_columns, f"{filename} のテーブルレイアウトが変更されました。{page}ページ目"

        df.columns = [column[1] for column in layout]

        # Remove unnecessary columns
        for _, key, required in layout:
            if not required:
                del df[key]

        df_cleansed = df.applymap(removeNewLine)

        df_cleansed["category"] = category

        return df_cleansed

    def allergen_state_of(self, value: str) -> AllergenState:
        if value == "●":
            return AllergenState.CONTAIN
        elif value == "▲":
            return AllergenState.MAY_CONTAIN
        elif numpy.isnan(value):
            return AllergenState.NOT_CONTAIN
        else:
            raise ValueError(f"Unknown AllergenState {value}.")
