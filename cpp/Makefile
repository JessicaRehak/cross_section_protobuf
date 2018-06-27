
default_target: protobuf_test

material.pb.cc material.pb.h: ../proto/material.proto
	protoc --cpp_out=$(PWD) -I=../proto/ ../proto/material.proto

protobuf_test: protobuf_test.cpp material.pb.cc material.pb.h
	c++ -o protobuf_test protobuf_test.cpp material.pb.cc `pkg-config --cflags --libs protobuf`
