import os
import sys

from scapywrapper.utilities.loggable import Loggable
from scapywrapper.pcapFileParser.pcapFileParser import PcapFileParser


class MainClass(Loggable):

    def __init__(self):
        Loggable.__init__(self, self.__class__.__name__)
        print(self.log_me())

    def create_pcap_file_parser_for_pcap_file(self, pcap_file):
        if pcap_file is None:
            print(self.log_me() + "the pcap file that was provides is None")
            return None

        if not os.path.isfile(pcap_file):
            print(self.log_me() + "the given pcap file does not exist")
            return None

        return PcapFileParser(pcap_file)



if __name__ == "__main__":
    func_name = "main - "
    print(func_name + "start")
    main_obj = MainClass()
    print(func_name + "got command line arguments:\n" + str(sys.argv))
    pcap_file_parser = main_obj.create_pcap_file_parser_for_pcap_file(sys.argv[1])
    packet_num = 2
    packet_data = pcap_file_parser.get_specific_packet(packet_num)

    print(func_name + "end")
