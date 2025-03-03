# /// script
# dependencies = [
#   "grpcio-tools>=1.70.0",
# ]
# ///

"""
Add orders

When an order is filled, another response is sent from `trade.psex.io:50051` with the filled order details.
This is not currently fetched in this script. (We only read 1 response per order placed)
To effectively fetch these, asynchronously read the responses in a loop separately to sending orders.
"""

import asyncio
from datetime import datetime
import logging
import grpc.aio

import common_pb2 as common_pb2
import port_pb2 as port_pb2
import port_pb2_grpc as port_pb2_grpc


async def run():
    # Define your API key
    api_key_1 = "00000000-0000-4000-a000-000000000001"

    # Prepare metadata with the API key (used for authentication)
    metadata = (("api-key", api_key_1),)

    print("Connecting to server...")
    # Create secure channel credentials (defaults are used here)
    async_channel = grpc.aio.insecure_channel("trade.psex.io:50051")
    # async_channel = grpc.aio.insecure_channel("localhost:50052")

    async with async_channel as channel:
        stub = port_pb2_grpc.PortServiceStub(channel)
        response = await stub.CancelAllOrders(common_pb2.Empty(), metadata=metadata)
        print(
            "positions",
            response,
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
