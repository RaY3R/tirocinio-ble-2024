from SnifferAPI import UART
from nrf_aggregator import NRFSniffersAggregator
import logging

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
        
        aggregator.feed_wireshark()
        
    except KeyboardInterrupt:
        aggregator.quit()
    except Exception as e:
        logging.error("Unhandled exception", exc_info=e)
        aggregator.quit()