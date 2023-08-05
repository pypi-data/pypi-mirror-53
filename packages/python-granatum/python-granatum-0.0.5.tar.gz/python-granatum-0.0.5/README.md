# python-granatum

## Introduction

**python-granatum** is a Python wrapper for [Granatum Financeiro](https://www.granatum.com.br/financeiro/).

## Quick Start

Fill in the <values> in this script to get a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) representation of transactions for a given account.
```
from datetime import date

from granatum import Granatum


end_date = date(2019, 8, 31)
start_date = date(2019, 8, 1)
filters = {'conta_id': ['<name of the account>']}

granatum = Granatum()
granatum.login('<email>', '<password>')
granatum.exportar(end_date, start_date, filters, 'pandas.DataFrame')
```
