# cross_section_protobuf
A cross-section file format for nuclear data cross-sections using
Google protocol buffers.

- `proto`: `.proto` files
- `python`: python scripts for converting `.xml` material data files
  into the protocol buffer format
- `lib`: library of cross-section data divided by benchmark and
  format.
  
Compile protocol buffer using:
```
protoc --python_out=./python/proto/ -I=./proto./proto/material_protobuf.proto
```

Requires:

- [Google protocol buffers](https://github.com/google/protobuf)
