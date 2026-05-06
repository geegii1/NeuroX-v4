from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

API_KEY = "PKQRIXAXVIPNKXE7FJHPSXS3SE"
API_SECRET = "14fKSkkYhvw15FmGb2zrkAWc2qAsgGMAERmLrm9WpyCB"


class AlpacaExecutor:
    def __init__(self):
        self.trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
        self.data_client = StockHistoricalDataClient(API_KEY, API_SECRET)

    def place_order(self, symbol, qty, side):
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )
        return self.trading_client.submit_order(order_data)

    def get_order_status(self, order_id):
        order = self.trading_client.get_order_by_id(order_id)
        return order.status

    def get_latest_price(self, symbol):
        request = StockLatestQuoteRequest(symbol_or_symbols=[symbol])
        quote = self.data_client.get_stock_latest_quote(request)

        bid = quote[symbol].bid_price
        ask = quote[symbol].ask_price

        return (bid + ask) / 2
