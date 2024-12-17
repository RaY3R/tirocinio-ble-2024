from scapy.contrib.nrf_sniffer import *
from ..aggregator import NRFSniffersAggregator
from ..SnifferAPI import UART
import logging
import time

if __name__ == "__main__":
    # setup logger
    logging.basicConfig(level=logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.root.addHandler(handler)
    
    try:
        
        ports = UART.find_sniffer()
        aggregator = NRFSniffersAggregator(port_list=ports, adv_channels=[37,38,39])
        aggregator.setup()
        aggregator.run()
        
        while True:
            packets = aggregator.get_packets()
            for p in packets:
                scapy_packet = NRFS2_Packet(p)
                print(scapy_packet.summary())
            time.sleep(0.1)
        
    except KeyboardInterrupt:
        aggregator.quit()
    except Exception as e:
        logging.error("Unhandled exception", exc_info=e)
        aggregator.quit()