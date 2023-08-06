from typing import Optional

import pandas as pd
from contracts import contract

from .._settings import _MONTHS_PER_YEAR
from .._sources.inflation_source import InflationSource
from .._sources.single_financial_symbol_source import CbrCurrenciesSource
from ..common.enums import Currency
from ..common.financial_symbol import FinancialSymbol
from ..common.time_series import TimeSeries, TimeSeriesKind


class PortfolioCurrency:

    def __init__(self,
                 inflation_source: InflationSource,
                 cbr_currencies_source: CbrCurrenciesSource,

                 currency: Currency):
        self.cbr_currencies_source = cbr_currencies_source
        self.inflation_source = inflation_source

        self._currency = currency

        inflation_symbol = self.inflation_source.fetch_financial_symbol(currency.name)
        if inflation_symbol is None:
            raise ValueError('Inflation symbol for the `name`={} is not found'.format(currency.name))
        self._inflation_symbol: FinancialSymbol = inflation_symbol

        currency_symbol = self.cbr_currencies_source.fetch_financial_symbol(currency.name)
        if currency_symbol is None:
            raise ValueError('Currency symbol for the `name`={} is not found'.format(currency.name))
        self._currency_symbol: FinancialSymbol = currency_symbol
        self._period_min: pd.Period = max(
            self.inflation_start_period - 1,
            self._currency_symbol.start_period.asfreq(freq='M'),
        )
        self._period_max: pd.Period = min(
            self.inflation_end_period,
            self._currency_symbol.end_period.asfreq(freq='M'),
        )

    @property
    def period_min(self) -> pd.Period:
        return self._period_min

    @property
    def period_max(self) -> pd.Period:
        return self._period_max

    @property
    def inflation_start_period(self) -> pd.Period:
        return self._inflation_symbol.start_period.asfreq(freq='M')

    @property
    def inflation_end_period(self) -> pd.Period:
        return self._inflation_symbol.end_period.asfreq(freq='M')

    @property
    def value(self) -> Currency:
        return self._currency

    @contract(
        kind='str',
        years_ago='int,>0|None',
    )
    def inflation(self, kind: str,
                  end_period: pd.Period,
                  start_period: pd.Period = None,
                  years_ago: Optional[int] = None) -> Optional[TimeSeries]:
        """
        Computes the properly reduced inflation for the currency

        :param start_period:
            the period from which the inflation is calculated
        :param end_period:
            the period to which the inflation is calculated
            is computed automatically if `years_ago` is provided
        :param years_ago:
            years back from `period_max` to calculate inflation

        :param kind:
            cumulative - cumulative inflation

            a_mean - arithmetic mean of inflation

            g_mean - geometric mean of inflation

            yoy - Year on Year inflation

            values - raw values of inflation
        :return:
        """
        if (years_ago is None) == (start_period is None):
            raise ValueError('either `start_period` or `years_ago` should be provided')

        if years_ago is not None:
            start_period = end_period - years_ago * _MONTHS_PER_YEAR + 1

        inflation_values = self._inflation_symbol.values(start_period=start_period,
                                                         end_period=end_period)

        inflation_ts = TimeSeries(values=inflation_values.value.values,
                                  start_period=inflation_values.period.min(),
                                  end_period=inflation_values.period.max(),
                                  kind=TimeSeriesKind.DIFF)

        def __cumulative():
            return (inflation_ts + 1.).prod() - 1.

        if kind == 'cumulative':
            return __cumulative()
        elif kind == 'yoy':
            return inflation_ts.ytd()
        elif kind == 'cumulative_series':
            return (inflation_ts + 1.).cumprod() - 1.
        elif kind == 'a_mean':
            inflation_amean = inflation_ts.mean()
            return inflation_amean
        elif kind == 'g_mean':
            years_total = inflation_ts.period_size / _MONTHS_PER_YEAR
            if years_total < 1.:
                return None
            inflation_gmean = (__cumulative() + 1.) ** (1 / years_total) - 1.
            return inflation_gmean
        elif kind == 'values':
            return inflation_ts
        else:
            raise ValueError('inflation kind is not supported: {}'.format(kind))

    def __repr__(self) -> str:
        currency_repr = 'Currency({})'.format(self._currency.name)
        return currency_repr


class PortfolioCurrencyFactory:

    def __init__(self,
                 inflation_source: InflationSource,
                 cbr_currencies_source: CbrCurrenciesSource):
        self.inflation_source = inflation_source
        self.cbr_currencies_source = cbr_currencies_source

    def new(self, currency: Currency) -> PortfolioCurrency:
        return PortfolioCurrency(inflation_source=self.inflation_source,
                                 cbr_currencies_source=self.cbr_currencies_source,
                                 currency=currency)
