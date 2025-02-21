# /// script
# dependencies = [
#   "grpcio-tools>=1.70.0",
# ]
# ///


import asyncio
from datetime import datetime
import logging
import random
import grpc.aio

import proto.common_pb2 as common_pb2
import proto.port_pb2 as port_pb2
import proto.port_pb2_grpc as port_pb2_grpc


async def run():
    # Define your API key
    api_key_1 = "00000000-0000-4000-a000-000000000000"

    # Prepare metadata with the API key
    # This is how authenticated connections are initialised
    metadata = (("api-key", api_key_1),)

    print("Connecting to server...")
    creds = grpc.ssl_channel_credentials(
        root_certificates=None, private_key=None, certificate_chain=None
    )
    async_channel = grpc.aio.secure_channel("trade.psex.io:443", creds)

    async with async_channel as channel:
        stub = port_pb2_grpc.PortServiceStub(channel)
        orders_stream = stub.StreamOrders(metadata=metadata)

        while True:
            request_buy = port_pb2.OrdersStreamRequest(
                add_order=port_pb2.AddOrderRequest(
                    symbol="AAPL",
                    side=random.choice(
                        [common_pb2.OrderDirection.BUY, common_pb2.OrderDirection.SELL]
                    ),
                    type=common_pb2.OrderType.LIMIT,
                    time_in_force=common_pb2.OrderTimeInForce.GFD,
                    quantity=random.randint(1, 100),
                    price=random.randint(90, 100),
                    timestamp=datetime.now(),
                    # client_order_id="123",
                )
            )
            await orders_stream.write(request_buy)
            response = await orders_stream.read()
            print(response)


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())
