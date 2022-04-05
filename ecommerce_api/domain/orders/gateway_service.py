import json

from requests import Response

from domain.gateway.gateway import Gateway
from domain.gateway.exceptions import (
    DollarBluePriceNotFoundError,
    DollarBluePriceIsZero,
)


class DollarValue:
    """Get dollar blue value of a product"""

    TIMEOUT = 10
    SELLER = 'casa'
    DOLLAR_TYPE = "nombre"
    DOLLAR_NAME = 'Dolar Blue'
    BUY_OR_SELL = 'venta'

    def __init__(self, dollarsi_gateway: Gateway):
        self._dollarsi_gateway = dollarsi_gateway

    def get_dollar_blue_values(self) -> Response:
        """Get the dollar blue value."""

        return self._dollarsi_gateway.post(timeout=self.TIMEOUT)

    def get_dollar_blue_price(self) -> float:
        dollar_value_response = self.get_dollar_blue_values()
        if len(dollar_value_response.text) == 0:
            raise DollarBluePriceNotFoundError()
        dollar_values = json.loads(dollar_value_response.text)
        try:
            for agency in dollar_values:
                if agency[self.SELLER][self.DOLLAR_TYPE] == self.DOLLAR_NAME:
                    return self._comma_value_to_float(agency[self.SELLER][self.BUY_OR_SELL])
        except KeyError:
            pass

        raise DollarBluePriceNotFoundError()

    def get_total_usd(self, total_order: float, dollar_blue_value: float) -> float:
        try:
            return total_order / dollar_blue_value
        except ZeroDivisionError:
            raise DollarBluePriceIsZero()

    def _comma_value_to_float(self, value: str) -> float:
        value.replace('.', '')
        return float(value.replace(',', '.'))
