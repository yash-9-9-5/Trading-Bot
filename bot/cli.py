import argparse
import sys

from bot.client import MockClient
from bot.orders import OrderManager
from bot.logging_config import logger

def main():
    parser = argparse.ArgumentParser(description="Mock Trading CLI (No Binance APIs)") # Set up command-line arguments for 
    
    parser.add_argument("--symbol", required=True, help="Trading pair symbol (e.g., BTCUSDT)") 
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side (BUY or SELL)")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, help="Amount to trade")
    parser.add_argument("--price", required=False, default="", help="Price (Required for LIMIT orders)")

    args = parser.parse_args()

    # No API Keys required 
    client = MockClient()
    order_manager = OrderManager(client)

    try:
        order_manager.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()
