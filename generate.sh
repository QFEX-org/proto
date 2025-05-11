#!/usr/bin/env bash
set -euo pipefail

PROTO_DIR=./proto

# ---- common ----
mkdir -p common
echo "Generating common/*.pb.go and common/*_pb2.py…"
protoc \
  --proto_path="$PROTO_DIR" \
  --go_out=paths=source_relative:common \
  --go-grpc_out=paths=source_relative:common \
  "$PROTO_DIR/common.proto"

python -m grpc_tools.protoc \
  --proto_path="$PROTO_DIR" \
  --python_out=common \
  --grpc_python_out=common \
  "$PROTO_DIR/common.proto"


# ---- market_data ----
mkdir -p market_data
echo "Generating market_data/*.pb.go and market_data/*_pb2.py…"
protoc \
  --proto_path="$PROTO_DIR" \
  --go_out=paths=source_relative:market_data \
  --go-grpc_out=paths=source_relative:market_data \
  "$PROTO_DIR/market_data.proto"

python -m grpc_tools.protoc \
  --proto_path="$PROTO_DIR" \
  --python_out=market_data \
  --grpc_python_out=market_data \
  "$PROTO_DIR/market_data.proto"


# ---- port ----
mkdir -p port
echo "Generating port/*.pb.go and port/*_pb2.py…"
protoc \
  --proto_path="$PROTO_DIR" \
  --go_out=paths=source_relative:port \
  --go-grpc_out=paths=source_relative:port \
  "$PROTO_DIR/port.proto"

python -m grpc_tools.protoc \
  --proto_path="$PROTO_DIR" \
  --python_out=port \
  --grpc_python_out=port \
  "$PROTO_DIR/port.proto"


# fix market_data imports
sed -i '' \
  -e 's|^import common_pb2 as common__pb2|from common import common_pb2 as common__pb2|' \
  -e 's|^import common_pb2$|from common import common_pb2|' \
  market_data/market_data_pb2.py \
  market_data/market_data_pb2_grpc.py

# fix port imports
sed -i '' \
  -e 's|^import common_pb2 as common__pb2|from common import common_pb2 as common__pb2|' \
  -e 's|^import common_pb2$|from common import common_pb2|' \
  port/port_pb2.py \
  port/port_pb2_grpc.py

sed -i '' \
  -e 's|^import market_data_pb2 as|from market_data import market_data_pb2 as|' \
  market_data/market_data_pb2_grpc.py

# fix port stub:
sed -i '' \
  -e 's|^import port_pb2 as|from port import port_pb2 as|' \
  port/port_pb2_grpc.py
