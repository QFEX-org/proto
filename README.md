# Examples

# Setup protobufs
Ensure you have `grpcio-tools` python package installed
```
python -m grpc_tools.protoc -I. --python_out=./examples --grpc_python_out=./examples market_data.proto
python -m grpc_tools.protoc -I. --python_out=./examples --grpc_python_out=./examples port.proto
python -m grpc_tools.protoc -I. --python_out=./examples --grpc_python_out=./examples common.proto
```

# Run script
Ensure you have [uv](https://docs.astral.sh/uv/guides/install-python/) python package manager installed
```
uv run examples/market_data_order_book.py
```