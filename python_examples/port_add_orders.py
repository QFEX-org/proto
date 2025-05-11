# /// script
# dependencies = [
#   "grpcio-tools>=1.70.0", "python-dotenv"
# ]
# ///

"""
Add orders

When an order is filled, another response is sent from `trade.psex.io:443` with the filled order details.
This is not currently fetched in this script. (We only read 1 response per order placed)
To effectively fetch these, asynchronously read the responses in a loop separately to sending orders.
"""

import asyncio
from datetime import datetime
import logging
import random
import grpc.aio

from common import common_pb2
from port import port_pb2, port_pb2_grpc
import os
from dotenv import load_dotenv

load_dotenv()


async def write_orders(orders_stream):
    """Continuously write orders to the stream."""
    while True:
        # request_buy = port_pb2.OrdersStreamRequest(
        #     modify_order=port_pb2.ModifyOrderRequest(
        #         symbol="SP500-USD", order_id="123", price=560.60, quantity=0.2
        #     )
        # )
        request_buy = port_pb2.OrdersStreamRequest(
            add_order=port_pb2.AddOrderRequest(
                symbol="SP500-USD",
                side=random.choice(
                    [common_pb2.OrderDirection.BUY, common_pb2.OrderDirection.SELL]
                ),
                type=common_pb2.OrderType.LIMIT,
                time_in_force=common_pb2.OrderTimeInForce.GFD,
                quantity=0.1,
                price=random.randint(450, 550),
                timestamp=datetime.now(),
            )
        )
        print(request_buy)
        await orders_stream.write(request_buy)
        # Pause briefly before sending the next order
        await asyncio.sleep(0.01)


async def read_responses(orders_stream):
    """Continuously read responses from the stream."""
    while True:
        try:
            response = await orders_stream.read()
            print("Received response:", response)
        except Exception as e:
            logging.error("Error reading response: %s", e)
            break  # Exit loop if the stream is closed or an error occurs


async def run():
    # Define your API key
    api_key_1 = os.getenv("QFEX_API_KEY")
    assert api_key_1
    # Prepare metadata with the API key (used for authentication)
    metadata = (("api-key", api_key_1),)

    print("Connecting to server...")
    # Create secure channel credentials (defaults are used here)
    creds = grpc.ssl_channel_credentials()
    async_channel = grpc.aio.secure_channel("trade.psex.io:443", creds)
    ###async_channel = grpc.aio.insecure_channel("localhost:50052")

    async with async_channel as channel:
        stub = port_pb2_grpc.PortServiceStub(channel)
        orders_stream = stub.StreamOrders(metadata=metadata)

        # Run writing and reading concurrently
        await asyncio.gather(write_orders(orders_stream), read_responses(orders_stream))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
