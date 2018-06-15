#include "proto/material_protobuf.pb.h"

#ifdef TEST
#include "gtest/gtest.h"
#endif

int main(int argc, char* argv[]) {
#ifdef TEST
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
#else
  std::cout << "XPT!" <<std::endl;
  return 0;
#endif
}
