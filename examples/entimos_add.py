# /// script
# dependencies = [
#   "grpcio-tools>=1.70.0",
# ]
# ///

import grpc

import common_pb2 as common_pb2
import market_data_pb2 as market_data_pb2
import market_data_pb2_grpc as market_data_pb2_grpc
import user_pb2 as user_pb2
import user_pb2_grpc as user_pb2_grpc

"""
TO RUN THIS FILE:

1. cd into parent directory
2. uv run examples/market_data_trades.py
"""


def run():
    creds = grpc.ssl_channel_credentials(
        root_certificates=None, private_key=None, certificate_chain=None
    )
    channel = grpc.insecure_channel("18.133.122.27:31451")
    channel = grpc.insecure_channel("localhost:50053")

    stub = user_pb2_grpc.BalanceServiceStub(channel)
    # api_key_sell = "c5f3ee4f-a747-4d54-a67e-7db3b405667d"
    request = user_pb2.DepositRequest(
#        user_id="dcbf9b4d-c5c1-4481-bcad-d8c82ab91242", deposit=10_000_000 * 10**8
         user_id="dcbf9b4d-c5c1-4481-bcad-d8c82ab91242", deposit=50 * 10**8
    )
    repsonse = stub.DepositBalance(request)
    print(f"Received data: {repsonse}")
    request = user_pb2.DepositRequest(
        user_id="6400005d-0afc-4dcc-b75c-69c1f74af25f", deposit=10_000_000 * 10**8
    )
    repsonse = stub.DepositBalance(request)
    # repsonse = stub.GetUserBalance(request, metadata=(("api-key", api_key_sell),))
    print(f"Received data: {repsonse}")


if __name__ == "__main__":
    run()

