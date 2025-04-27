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

import common_pb2 as common_pb2
import port_pb2 as port_pb2
import port_pb2_grpc as port_pb2_grpc
import os
from dotenv import load_dotenv
load_dotenv()

async def write_orders(orders_stream):
    """Continuously write orders to the stream."""
    while True:
        request_buy = port_pb2.OrdersStreamRequest(
            add_order=port_pb2.AddOrderRequest(
                symbol="SP500-USD",
                side=common_pb2.OrderDirection.SELL,
                type=common_pb2.OrderType.LIMIT,
                time_in_force=common_pb2.OrderTimeInForce.GFD,
                quantity=1,
                price=470,
                timestamp=datetime.now(),
            )
        )
        # print(request_buy)
        await orders_stream.write(request_buy)
        # Pause briefly before sending the next order
        await asyncio.sleep(60)


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
    api_key_1 = "a00fdce9-7d62-413b-b26c-42fa23717950" 
    # Prepare metadata with the API key (used for authentication)
    metadata = (("api-key", api_key_1),)

    print("Connecting to server...")
    # Create secure channel credentials (defaults are used here)
    creds = grpc.ssl_channel_credentials()
    async_channel = grpc.aio.secure_channel("trade.pfex.io:443", creds)
    async_channel = grpc.aio.insecure_channel("localhost:50052")


    async with async_channel as channel:
        stub = port_pb2_grpc.PortServiceStub(channel)
        orders_stream = stub.StreamOrders(metadata=metadata)

        # Run writing and reading concurrently
        await asyncio.gather(write_orders(orders_stream), read_responses(orders_stream))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
