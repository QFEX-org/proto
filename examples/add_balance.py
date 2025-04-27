# /// script
# dependencies = [
#   "grpcio-tools>=1.70.0","python-dotenv"
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


async def run():
    # Define your API key
    api_key_1 = os.getenv("PFEX_API_KEY")

    # Prepare metadata with the API key (used for authentication)
    metadata = (("api-key", api_key_1),)

    print("Connecting to server...")
    creds = grpc.ssl_channel_credentials()
    async_channel = grpc.aio.insecure_channel("localhost:50052")
    async_channel = grpc.aio.secure_channel("trade.psex.io:443", creds)
    async_channel = grpc.aio.secure_channel("trade.pfex.io:443", creds)

    async with async_channel as channel:
        stub = port_pb2_grpc.PortServiceStub(channel)
        response = await stub.DepositFunds(
            port_pb2.DepositRequest(
                user_id="adee97c9-a587-44c2-aab1-b8e933ef3ebd",
                deposit=5000_00000000,
            ),
            metadata=metadata,
        )
        print(
            "success",
            response,
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
