# sushi-allergy-parser

`sushi-allergy-parser` is a parser for allergy infomation document of japanese conveyor-belt sushi chain. Currently, the following documents are supported.

* スシロー (http://www3.akindo-sushiro.co.jp/pdf/menu/allergy.pdf)
* くら寿司 (http://www.kura-corpo.co.jp/common/pdf/kura_allergen.pdf)


## Requirements

`sushi-allergy-parser` depends on [tabula-py](https://github.com/chezou/tabula-py), so you should install Java(7 or 8).

## Installation

```sh
$ pip install sushi-allergy-parser
```

## Usage

```python
>>> from sushi_allergy_parser import SushiroAllergyParser
>>> df = SushiroAllergyParser().parse()
>>> type(df)
<class 'pandas.core.frame.DataFrame'>
>>> df
    category       name          egg  ...      gelatin       sesame    cashewNut
0        にぎり  合鴨ロースの煮込み  NOT_CONTAIN  ...  NOT_CONTAIN  NOT_CONTAIN  NOT_CONTAIN
1        にぎり        赤えび  NOT_CONTAIN  ...  NOT_CONTAIN  NOT_CONTAIN  NOT_CONTAIN
2        にぎり         あじ  NOT_CONTAIN  ...  NOT_CONTAIN  NOT_CONTAIN  NOT_CONTAIN
3        にぎり  あじ(ネギ・生姜)  NOT_CONTAIN  ...  NOT_CONTAIN  NOT_CONTAIN  NOT_CONTAIN
4        にぎり   穴子天ぷらにぎり  MAY_CONTAIN  ...  MAY_CONTAIN  MAY_CONTAIN  NOT_CONTAIN
..       ...        ...          ...  ...          ...          ...          ...
319      その他        天つゆ  NOT_CONTAIN  ...  MAY_CONTAIN  MAY_CONTAIN  NOT_CONTAIN
320      その他       粉末緑茶  NOT_CONTAIN  ...  NOT_CONTAIN  NOT_CONTAIN  NOT_CONTAIN
321      その他        ぽん酢  NOT_CONTAIN  ...  NOT_CONTAIN  MAY_CONTAIN  NOT_CONTAIN
322      その他        わかめ  NOT_CONTAIN  ...  NOT_CONTAIN  NOT_CONTAIN  NOT_CONTAIN
323      その他        わさび  MAY_CONTAIN  ...  MAY_CONTAIN  NOT_CONTAIN  NOT_CONTAIN
```
