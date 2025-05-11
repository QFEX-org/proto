# /// script
# dependencies = [
#   "grpcio-tools>=1.70.0",
# ]
# ///

import grpc

from common import common_pb2
from market_data import market_data_pb2, market_data_pb2_grpc

"""
TO RUN THIS FILE:

1. cd into parent directory
2. uv run examples/market_data_order_book.py
"""


def run():
    creds = grpc.ssl_channel_credentials(
        root_certificates=None, private_key=None, certificate_chain=None
    )
    channel = grpc.secure_channel("mds.pfex.io:443", creds)

    stub = market_data_pb2_grpc.MarketDataServiceStub(channel)

    request = market_data_pb2.GetSymbol(symbol="SP500-USD")
    for response in stub.GetOrderBook(request):
        print(f"Received data: {response}")


if __name__ == "__main__":
    run()
