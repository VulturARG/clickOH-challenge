import unittest
from unittest.mock import Mock

from domain.gateway.dolarsi_gateway import DollarURLGateway
from domain.gateway.exceptions import DollarBluePriceNotFoundError, DollarBluePriceIsZero
from domain.orders.gateway_service import DollarValue


class GatewayServiceTestCase(unittest.TestCase):
    def setUp(self):

        self.mock_server_gateway = Mock(spec=DollarURLGateway)
        self.dollar_value = DollarValue(self.mock_server_gateway)

    def test_get_dollar_blue_price(self):
        api_response = '[{"casa":{"venta":"199,00","nombre":"Dolar Blue"}}]'
        # values returned by the repository
        self.mock_server_gateway.post.return_value.text = api_response

        actual = self.dollar_value.get_dollar_blue_price()
        self.assertEqual(199, actual)

    def test_get_dollar_blue_price_not_found(self):
        api_response = '[{"casa": {"nombre": "Dolar Oficial"}}]'
        # values returned by the repository
        self.mock_server_gateway.post.return_value.text = api_response

        with self.assertRaises(DollarBluePriceNotFoundError):
            self.dollar_value.get_dollar_blue_price()

    def test_get_dollar_blue_price_key_error(self):
        api_response = '[{"bad_name": {"nombre": "Dolar Oficial"}}]'
        # values returned by the repository
        self.mock_server_gateway.post.return_value.text = api_response

        with self.assertRaises(DollarBluePriceNotFoundError):
            self.dollar_value.get_dollar_blue_price()

    def test_get_total_usd(self):
        actual = self.dollar_value.get_total_usd(total_order=400, dollar_blue_value=200)
        self.assertEqual(2, actual)

    def test_get_total_usd_dollar_blue_is_zero(self):
        with self.assertRaises(DollarBluePriceIsZero):
            actual = self.dollar_value.get_total_usd(total_order=400, dollar_blue_value=0)
