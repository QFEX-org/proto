# /// script
# dependencies = [
#   "grpcio-tools>=1.70.0","python-dotenv"
# ]
# ///

"""
Add orders

When an order is filled, another response is sent from `trade.qfex.com:443` with the filled order details.
This is not currently fetched in this script. (We only read 1 response per order placed)
To effectively fetch these, asynchronously read the responses in a loop separately to sending orders.
"""

import asyncio
import logging
import grpc.aio

from common import common_pb2
from port import port_pb2, port_pb2_grpc
import os
from dotenv import load_dotenv

load_dotenv()


async def run():
    # Define your API key
    api_key_1 = os.getenv("QFEX_API_KEY")

    # Prepare metadata with the API key (used for authentication)
    metadata = (("api-key", api_key_1),)

    print("Connecting to server...")
    creds = grpc.ssl_channel_credentials()
    async_channel = grpc.aio.secure_channel("trade.qfex.com:443", creds)
    # async_channel = grpc.aio.insecure_channel("localhost:50052")

    async with async_channel as channel:
        stub = port_pb2_grpc.PortServiceStub(channel)
        response = await stub.GetAvailableLeverageLevels(
            common_pb2.ListRequest(limit=1000, offset=0), metadata=metadata
        )
        print(
            "available leverages",
            response,
        )
        response = await stub.GetUserLeverage(
            common_pb2.ListRequest(limit=1000, offset=0), metadata=metadata
        )
        print("user leverages", response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
