# install cargo if not


#!/bin/bash
pip install -r ./requirements.txt
# gen python grpc things
[ -d "./python-grpc" ] ||  mkdir ./python-grpc
python -m grpc_tools.protoc -I ./rust-grpc/ --python_out=./python-grpc \
         --grpc_python_out=./python-grpc ./rust-grpc/proto/helloworld.proto
# setup grpc rsqlulte rust server
cd rust-grpc
cargo build --bin server
