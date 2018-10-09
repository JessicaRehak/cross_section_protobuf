#!/usr/bin/env python3

import material_pb2
import sys
from google.protobuf import text_format

if len(sys.argv) != 2:
    print("Usage: " + str(sys.argv[0]) + " ASCII_FILE_TO_CONVERT");
    sys.exit()

new_material = material_pb2.Material()
filename = str(sys.argv[1])

# Read file
f = open(filename, "rb")
text_format.Parse(f.read(), new_material)
f.close()

# Write protobuf

f = open(filename + "_converted.material", "wb")
f.write(new_material.SerializeToString())
f.close()
