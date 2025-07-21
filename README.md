# Getting started

## Prerequisites

- [Python](https://www.python.org/downloads/)
- Python package manager (e.g., [pip](https://pypi.org/project/pip/))
- [grpc](https://grpc.io/docs/languages/cpp/quickstart/) (e.g., with brew on macOS)
- [go](https://go.dev/doc/install) (e.g., with brew on macOS)

## Setup environment

1. Add your project root to `PYTHONPATH`:
```
export PYTHONPATH=$PWD
```

2. Install the gRPC packages:
```sh
python -m pip install grpcio-tools
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

3. Generate your Python stubs:
```sh
./generate.sh
```

## Run example scripts

Run the market data order book example. Use one of the following:
```sh
python python_examples/market_data_order_book.py 
```

# Other examples

Please see [our docs](https://docs.qfex.com/) for more examples.