from functools import lru_cache
from typing import Optional, Callable

import pandas as pd

from .base_classes import FinancialSymbolsSource
from .._settings import data_url
from ..common.enums import Currency, SecurityType, Period
from ..common.financial_symbol import FinancialSymbol
from ..common.financial_symbol_id import FinancialSymbolId
from ..common.financial_symbol_info import FinancialSymbolInfo


class YahooIndexesSource(FinancialSymbolsSource):
    def __init__(self):
        super().__init__(namespace='index')
        self.url_base = data_url + 'index/yahoo/'

        self.index = pd.read_csv(self.url_base + '__index.csv', sep='\t', index_col='name')
        self.index['date_start'] = pd.to_datetime(self.index['date_start']).dt.to_period(freq='D')
        self.index['date_end'] = pd.to_datetime(self.index['date_end']).dt.to_period(freq='D')

    @lru_cache(maxsize=512)
    def __extract_values(self, row_id: str) -> Callable[[pd.Period, pd.Period], pd.DataFrame]:
        def func(start_period: pd.Period, end_period: pd.Period) -> pd.DataFrame:
            url = '{}{}.csv'.format(self.url_base, row_id)
            df = pd.read_csv(url, sep='\t', parse_dates=['date'])
            df['period'] = df['date'].dt.to_period(freq='M')
            df_new = df[(start_period <= df['period']) & (df['period'] <= end_period)].copy()
            return df_new

        return func

    def fetch_financial_symbol(self, name: str) -> Optional[FinancialSymbol]:
        if name not in self.index.index:
            return None
        row = self.index.loc[name]
        symbol = FinancialSymbol(identifier=FinancialSymbolId(namespace=self.namespace, name=name),
                                 values=self.__extract_values(name),
                                 start_period=row['date_start'],
                                 end_period=row['date_end'],
                                 currency=Currency.USD,
                                 security_type=SecurityType.INDEX,
                                 period=Period.DAY,
                                 adjusted_close=True)
        return symbol

    def get_all_infos(self):
        infos = []
        for idx, row in self.index.iterrows():
            fin_sym_info = FinancialSymbolInfo(
                fin_sym_id=FinancialSymbolId(self.namespace, str(idx)),
                short_name=None,
            )
            infos.append(fin_sym_info)
        return infos
