# takes an XML file as command line argument 1 and a path (default .) as arg 2
# converts XML file to serialized material property file
# made from "XML Conversion.ipynb"
# assumes protoc has already been called
# usage example:
# ls ../lib/kaist/xml/*.xml | xargs -I '{}' python3 XML_To_Material.py '{}' ../lib/kaist/serialized/

import sys
import os
import xml.etree.cElementTree as ET
import proto.material_pb2 as mat_proto

def XML_To_Material(inputFilename):
	data = {}
	root = ET.parse(inputFilename).getroot()

	for el in root.findall('./material/'):
	    if el.tag == "prop":
	        prop_root = el
	    elif el.tag == "grp_structures":
	        grp_structs = el
	    else:
	        data.update({el.tag: el.text})

	for el in grp_structs[0]:
	    if el.tag == "chi":
	        data.update({"chi": [float(v) for v in el.text.split(',')]})
	    elif el.tag == "energy_groups":
	        data.update({"energy_groups": [float(v) for v in el.text.split(',')]})
	    elif el.tag == "xsec":
	        xsec_root = el

	for el in xsec_root:
	    if el.tag == "sig_s":
	        sig_s_root = el
	    else:
	        data.update({el.tag: [float(v) for v in el.text.split(',')]})

	#flatten matrix to 1D
	data.update({"sig_s": [float(v) for v in sig_s_root.text.replace('\n\t','').replace(';',',').split(',')]})

	material = mat_proto.Material()

	material.full_name = data["name"]
	material.id = data["id"]
	material.abbreviation = data["id"]

	key_map = {"energy_groups": mat_proto.Material.ENERGY_GROUPS,
	          "sig_t": mat_proto.Material.SIGMA_T,
	          "sig_a": mat_proto.Material.SIGMA_A,
	          "chi": mat_proto.Material.CHI,
	          "nu_sig_f": mat_proto.Material.NU_SIG_F,
	          "kappa_sig_f": mat_proto.Material.KAPPA_SIG_F}

	vector_properties = []
	for key, value in key_map.items():
	    vector_prop = mat_proto.Material.VectorProperty()
	    vector_prop.id = value
	    vector_prop.value.extend(data[key])
	    vector_properties.append(vector_prop)

	material.vector_property.extend(vector_properties)

	sig_s_matrix = mat_proto.Material.MatrixProperty()
	sig_s_matrix.id = mat_proto.Material.SIGMA_S
	sig_s_matrix.value.extend(data["sig_s"])

	material.matrix_property.extend([sig_s_matrix])

	return material


def main():
	inFile = sys.argv[1] #first command line argument
	if len(sys.argv) < 3:
		outPath = "."
	else:
		outPath = sys.argv[2] #second command line argument
	
	inPath, inFileName = os.path.split(inFile)

	if inFileName[-4:] == ".xml":
		outFileName = inFileName[:-4] + ".material"
	else:
		outFileName = inFileName + ".material"

	outFile = outPath + "/" + outFileName

	material = XML_To_Material(inFile)

	f = open(outFile, 'wb')
	f.write(material.SerializeToString())
	f.close()

	print("done writing " + outFile)

if __name__ == "__main__":
    main()