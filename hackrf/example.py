from decoder import HackrfDecoderBLE
import logging
import time

if __name__ == "__main__":
    
    # setup logger
    logging.basicConfig(level=logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.root.addHandler(handler)
    
    # Crea e avvia il decoder
    ble_decoder = HackrfDecoderBLE()
    ble_decoder.start_adv_hopping([37, 38, 39], interval=0.3)
    #ble_decoder.set_channel(39)
    ble_decoder.start()
    ble_decoder.sniff()
    print("Acquisizione BLE avviata. Premere Ctrl+C per interrompere.")
    ble_decoder.feed_wiresharsk()
    
    try:
        while True:
            for pkt in ble_decoder.get_packets():
                print(pkt.summary())
            time.sleep(0.1)
    
    except Exception as e:
        logging.error("Unahdled exception." ,exc_info=e)
    
    finally:
        ble_decoder.stop()
        ble_decoder.wait()