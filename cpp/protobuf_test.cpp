#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include "material.pb.h"

int main(int argc, char* argv[])
{
	GOOGLE_PROTOBUF_VERIFY_VERSION;

	Material material;

	std::ifstream inputFileStream(argv[1], std::ios::binary);

	if (!material.ParseFromIstream(&inputFileStream)) {
		std::cout << "failed to parse\n";
	}
	inputFileStream.close();

	std::cout << material.DebugString() << std::endl;

	std::map<Material::VectorId, std::vector<double>> vectorProperties;

	for (const auto& vecProp : material.vector_property()) {
		if (vecProp.id() == Material::UNKNOWN_VECTOR) {
			std::cout << "problem: got UNKNOWN_VECTOR\n";
		}
		else {
			std::vector<double> newVector(vecProp.value().cbegin(), vecProp.value().cend());
			vectorProperties.emplace(vecProp.id(), newVector);
		}
	}

	for (const auto& mapVal : vectorProperties) {
		std::cout << Material_VectorId_descriptor()->value(mapVal.first)->name() << std::endl;
		for (const auto& val : mapVal.second) {
			std::cout << val << ", ";
		}
		std::cout << std::endl;
	}

	return 0;
}
