.PHONY: proto clean

proto:
	@echo "🛠️  Generating protobuf code..."
	python3 -m grpc_tools.protoc \
		-I proto \
		--python_out=client \
		--grpc_python_out=client \
		proto/interactor.proto

	@echo "🔧 Fixing import in *_pb2_grpc.py..."
	sed -i 's/^import interactor_pb2/from . import interactor_pb2/' client/interactor_pb2_grpc.py

clean:
	rm -f client/interactor_pb2.py client/interactor_pb2_grpc.py