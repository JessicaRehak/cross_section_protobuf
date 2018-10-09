
default_target: python

.PHONY: python
python: ../proto/material.proto
	protoc --python_out=$(PWD) -I=../proto/ ../proto/material.proto

.PHONY: clean
clean:
	rm material_pb2.py
