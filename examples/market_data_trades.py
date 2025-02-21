# /// script
# dependencies = [
#   "grpcio-tools>=1.70.0",
# ]
# ///

import grpc

import common_pb2 as common_pb2
import market_data_pb2 as market_data_pb2
import market_data_pb2_grpc as market_data_pb2_grpc

"""
TO RUN THIS FILE:

1. cd into parent directory
2. uv run examples/market_data_trades.py
"""


def run():
    creds = grpc.ssl_channel_credentials(
        root_certificates=None, private_key=None, certificate_chain=None
    )
    channel = grpc.secure_channel("mds.psex.io:443", creds)

    stub = market_data_pb2_grpc.MarketDataServiceStub(channel)

    request = market_data_pb2.GetSymbol(symbol="AAPL")
    for response in stub.GetTrades(request):
        print(f"Received data: {response}")


if __name__ == "__main__":
    run()
