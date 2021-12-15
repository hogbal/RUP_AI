#include <iostream>
#include <vector>
#include "tkdnn.h"
#include "test.h"
#include "DarknetParser.h"

int main() {
	std::string bin_path = "/root/tkDNN/darknet";
	std::vector<std::string> input_bins = {
		bin_path + "/layers/input.bin"
	};
	std::vector<std::string> output_bins = {
		bin_path + "/debug/layer144_out.bin",
		bin_path + "/debug/layer159_out.bin",
		bin_path + "/debug/layer174_out.bin"
	};
	std::string wgs_path = bin_path + "/layers";
	std::string cfg_path = "/rup/setting/yolov4-csp/yolov4-csp.cfg";
	std::string name_path = "/rup/data/obj.names";

	downloadWeightsifDoNotExist(input_bins[0], bin_path, "https://cloud.hipert.unimore.it/s/AfzHE4BfTeEm2gH/download");

	tk::dnn::Network *net = tk::dnn::darknetParser(cfg_path, wgs_path, name_path);
	net->print();

	tk::dnn::NetworkRT *netRT = new tk::dnn::NetworkRT(net ,net->getNetworkRTName(bin_path.c_str()));

	int ret = testInference(input_bins, output_bins, net, netRT);
	net->releaseLayers();
	delete net;
	delete netRT;
	return ret;
}
