import random
import time
from bot.client import MockClient
from bot.logging_config import logger
from bot.validators import (
    validate_symbol, validate_side, validate_type,
    validate_quantity, validate_price, ValidationError
)

class OrderManager: # order manager to handle order placement logic, validation, and logging
    def __init__(self, client: MockClient):
        self.client = client

    def place_order(self, symbol: str, side: str, order_type: str, quantity: str, price: str = ""):
        """
        Validates inputs and places a simulated REST order.
        """
        try:
            logger.info("--- New Mock Order Request ---")
            
            # Validation
            v_symbol = validate_symbol(symbol)
            v_side = validate_side(side)
            v_type = validate_type(order_type)
            v_qty = validate_quantity(quantity)
            v_price = validate_price(price, v_type)

            # Parameter Construction
            params = {
                "symbol": v_symbol,
                "side": v_side,
                "type": v_type,
                "quantity": v_qty,
            }
            if v_type == "LIMIT":
                params["price"] = v_price

            logger.info("Validation passed. Sending mock REST direct order...")
            
            # Send direct REST call to a generic endpoint (httpbin)
            response = self.client._request("POST", "/post", params)

            # httpbin returns sent data under the "json" key
            sent_data = response.get("json", {})

            # Simulate a successful exchange response
            order_id = random.randint(100000, 999999)
            status = "FILLED" if v_type == "MARKET" else "NEW"
            
            logger.info("Order Placed Successfully via Direct REST Call!")
            logger.info(f"Mock Order ID: {order_id}")
            logger.info(f"Status: {status}")
            logger.info(f"Sent Symbol: {sent_data.get('symbol')}")
            logger.info(f"Sent Qty: {sent_data.get('quantity')}")

            return response

        except ValidationError as e:
            logger.error(f"Validation Failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Order Placement Failed: {e}")
            raise
