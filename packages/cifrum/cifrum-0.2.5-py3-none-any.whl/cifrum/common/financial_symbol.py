import datetime as dtm
from collections import namedtuple
from typing import Optional, Callable

import pandas as pd
from dateutil import relativedelta

from ..common.enums import Period, Currency, SecurityType
from ..common.financial_symbol_id import FinancialSymbolId


class ValuesFetcher:

    _PeriodRange = namedtuple('PeriodRange', 'start, end')

    def __init__(self, values_func, period_min, period_max):
        self._values_func = values_func
        self._period_min = period_min
        self._period_max = period_max
        self._current_period_start = None
        self._current_period_end = None
        self._values = None

    @property
    def _period_range(self):
        return self._PeriodRange(self._current_period_start, self._current_period_end)

    def _fetch(self, start_period: pd.Period, end_period: pd.Period):
        start_period = max(start_period, self._period_min)
        end_period = min(end_period, self._period_max)

        if self._current_period_start is None or \
                (start_period < self._current_period_start and end_period > self._current_period_end):
            self._current_period_start = start_period
            self._current_period_end = end_period
            self._values = self._values_func(start_period, end_period)

        elif start_period >= self._current_period_start and end_period <= self._current_period_end:
            pass

        elif start_period < self._current_period_start:
            self._values = self._values_func(start_period, self._current_period_start - 1).append(self._values)
            self._current_period_start = start_period

        elif end_period > self._current_period_end:
            self._values = self._values.append(self._values_func(self._current_period_end + 1, end_period))
            self._current_period_end = end_period

        else:
            pass

        periods = self._values.date.dt.to_period(freq='M')
        df = self._values[(start_period <= periods) & (periods <= end_period)]
        return df.copy()


class FinancialSymbol:
    def __init__(self,
                 identifier: FinancialSymbolId,
                 values: Callable[[pd.Period, pd.Period], pd.DataFrame],
                 adjusted_close: bool,
                 currency: Currency,
                 period: Period,
                 security_type: SecurityType,
                 start_period: Optional[pd.Period] = None,
                 end_period: Optional[pd.Period] = None,
                 isin: Optional[str] = None,
                 short_name: Optional[str] = None,
                 long_name: Optional[str] = None,
                 exchange: Optional[str] = None):
        self.identifier = identifier
        self.__values_fetcher = ValuesFetcher(
            values_func=values,
            period_min=pd.Period(start_period, freq='M'),
            period_max=pd.Period(end_period, freq='M')
        )
        self.isin = isin
        self.short_name = short_name
        self.long_name = long_name
        self.exchange = exchange
        self.currency = currency
        self.security_type = security_type
        self._start_period = start_period
        self._end_period = end_period
        self.period = period
        self.adjusted_close = adjusted_close

    def values(self, start_period: pd.Period, end_period: pd.Period) -> pd.DataFrame:
        vals = self.values_fetcher._fetch(start_period=start_period, end_period=end_period)

        if self.period == Period.DAY:
            # we are interested in day-time data as follows
            # - if there is no data for month or more (ticker is dead, probably), we drop all data for
            #   the last available period
            # - we drop data for the period of the current month
            # - for every period we take the value that is last in each month

            if 'period' not in vals.columns:
                vals['period'] = vals['date'].dt.to_period(freq='M')

            month_ago = pd.Period(dtm.datetime.now() - relativedelta.relativedelta(months=1), freq='D')
            if self.end_period < month_ago:
                vals = vals[vals['period'] < pd.Period(self.end_period, freq='M')]
            indicator__not_current_period = vals['period'] != pd.Period.now(freq='M')
            indicator__lastdate_indices = vals['period'] != vals['period'].shift(1)
            vals = vals[indicator__lastdate_indices & indicator__not_current_period].copy()
            del vals['date']
        elif self.period == Period.MONTH:
            del vals['date']
        elif self.period == Period.DECADE:
            vals = vals[vals['date'].dt.day == 3]
            vals['date'] = vals['date'].apply(lambda p: pd.Period(p, freq='M'))
            vals.rename(columns={'date': 'period'}, inplace=True)
        else:
            raise Exception('Unexpected type of `period`')

        vals.sort_values(by='period', ascending=True, inplace=True)
        return vals

    @property
    def start_period(self) -> pd.Period:
        if self._start_period is None:
            vals = self.values_fetcher._fetch(start_period=pd.Period('1900-1', freq='M'),
                                              end_period=pd.Period.now(freq='M'))
            self._start_period = vals['period'].min()
        return self._start_period

    @property
    def end_period(self) -> pd.Period:
        if self._end_period is None:
            vals = self.values_fetcher._fetch(start_period=pd.Period('1900-1', freq='M'),
                                              end_period=pd.Period.now(freq='M'))
            self._end_period = vals['period'].max()
        return self._end_period

    @property
    def values_fetcher(self) -> ValuesFetcher:
        return self.__values_fetcher

    @property
    def name(self) -> str:
        return self.identifier.name

    @property
    def namespace(self) -> str:
        return self.identifier.namespace

    @property
    def identifier_str(self) -> str:
        return self.identifier.format()

    def __repr__(self) -> str:
        repr = f'''
FinancialSymbol(identifier={self.identifier_str},
                start_period={self.start_period}, end_period={self.end_period}, period={self.period},
                currency={self.currency}, exchange={self.exchange},
                short_name={self.short_name}, long_name={self.long_name},
                isin={self.isin},
                security_type={self.security_type}, adjusted_close={self.adjusted_close})'''
        return repr
