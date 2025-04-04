import socket
from gnuradio import gr, blocks, filter, digital, analog
from gnuradio.filter import firdes
import osmosdr
from scapy.layers.bluetooth4LE import BTLE, BTLE_RF
import time
import numpy 
import queue
import threading
from utils import *
from constants import *

# Classe principale per l'acquisizione BLE
class HackrfDecoderBLE(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "BLE Decoder")
        
        self.packet_queue = queue.Queue()
        self.total_packets = 0
        self.crcEnabled = True
        self.crcInit = 0x555555

        # Configura HackRF come sorgente
        self.transition_width = transition_width = 300e3
        self.sample_rate = sample_rate = 20e6
        self.data_rate = data_rate = 1e6
        self.cutoff_freq = cutoff_freq = 1250e3
        self.ble_channel_spacing = ble_channel_spacing = 2e6
        self.ble_channel = ble_channel = 0
        self.ble_base_freq = ble_base_freq = 2402e6
        self.rf_gain = rf_gain = 100
        self.lowpass_filter = lowpass_filter = firdes.low_pass(1, sample_rate, cutoff_freq, transition_width)
        self.gmsk_sps = gmsk_sps = int(sample_rate/data_rate)
        self.gmsk_omega_limit = gmsk_omega_limit = 0.0002
        self.gmsk_mu = gmsk_mu = 0.5
        self.gmsk_gain_mu = gmsk_gain_mu = 0.175
        self.iq_output = iq_output = "/dev/null"
        self.freq_offset = freq_offset = 0
        self.freq = freq = ble_base_freq+(ble_channel_spacing * ble_channel)
        
        #self.unpacked_to_packed = blocks.unpacked_to_packed_bb(1, gr.GR_LSB_FIRST)
        self.rtlsdr_source_0 = osmosdr.source("numchan=1 hackrf=0")
        self.rtlsdr_source_0.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.rtlsdr_source_0.set_sample_rate(sample_rate)
        self.rtlsdr_source_0.set_center_freq((freq+freq_offset), 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(100, 0)
        self.rtlsdr_source_0.set_if_gain(89, 0)
        self.rtlsdr_source_0.set_bb_gain(0, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        
        self.simple_squelch_0 = analog.simple_squelch_cc(-100, 0.1)
        
        self.pfb_channelizer = filter.pfb.channelizer_ccf(
            numchans=10,
            taps=lowpass_filter,
            oversample_rate=1.0
        )
        
        self.connect((self.rtlsdr_source_0, 0), (self.simple_squelch_0, 0))
        self.connect((self.simple_squelch_0, 0), (self.pfb_channelizer, 0))
        
        self.demod_blocks = []
        self.unpacked_blocks = []
        self.sink_blocks = []

        for i in range(10):
            
            demod = digital.gfsk_demod(
                samples_per_symbol=gmsk_sps/10,
                sensitivity=((numpy.pi*2)/gmsk_sps),
                gain_mu=gmsk_gain_mu,
                mu=gmsk_mu,
                omega_relative_limit=gmsk_omega_limit,
                freq_error=0.0,
                verbose=False,
                log=False
            )
            self.demod_blocks.append(demod)
            
            unpacked = blocks.unpacked_to_packed_bb(1, gr.GR_LSB_FIRST)
            self.unpacked_blocks.append(unpacked)
            
            sink = blocks.vector_sink_b()
            self.sink_blocks.append(sink)
            
            self.connect((self.pfb_channelizer, i), (demod, 0))
            self.connect((demod, 0), (unpacked, 0))
            self.connect((unpacked, 0), (sink, 0))
        
        
    def get_data(self):
        channel_data = []
        for i, sink in enumerate(self.sink_blocks):
            # Ottiene i dati da ciascun sink e li associa all'indice del canale
            data = b''
            while len(data) < 1024:
                data += bytes(sink.data())
                
            if data:
                # Calcola il canale BLE fisico corrispondente a questo canale del channelizer
                ble_channel = self.calculate_ble_channel(i)
                channel_data.append((data, ble_channel))
            sink.reset()
        return channel_data

    def calculate_ble_channel(self, channelizer_index):

        # La frequenza centrale attualmente impostata
        center_freq = self.freq
        
        # Larghezza di banda totale coperta dal channelizer
        total_bandwidth = self.sample_rate
        
        # Larghezza di banda per canale del channelizer
        channel_bandwidth = total_bandwidth / 10  # 10 canali nel channelizer
        
        # Calcola la frequenza centrale di questo canale del channelizer
        # L'indice 0 è il canale più a sinistra (frequenza più bassa)
        channel_center_freq = center_freq - (total_bandwidth/2) + (channel_bandwidth/2) + (channelizer_index * channel_bandwidth)
        
        # Trova il canale BLE più vicino a questa frequenza
        nearest_ble_channel = round((channel_center_freq - self.ble_base_freq) / self.ble_channel_spacing)
        
        # Limita al range valido di canali BLE (0-39)
        nearest_ble_channel = max(0, min(39, nearest_ble_channel))
        
        return nearest_ble_channel

    def set_channel(self, channel, debug=True):
        
        self.freq = (channel * self.ble_channel_spacing + self.ble_base_freq)

        self.ble_channel = channel
        self.rtlsdr_source_0.set_center_freq((self.freq + self.freq_offset), 0) 
        if debug is True: print(f"Set channel to {channel} ({self.freq/1e6} MHz)")
    
    def adv_channel_to_physical(self, channel):
        if channel == 37:
            return 0
        elif channel == 38:
            return 12
        elif channel == 39:
            return 39
        
    def get_physical_channel(self, channel):
        if channel == 0:
            return 37
        elif channel == 12:
            return 38
        elif channel == 39:
            return 39
        else:
            return channel
    
    def start_adv_hopping(self, adv_channels=[37, 38, 39], interval=0.5):
        def _adv_hopping():
            while True:
                for channel in adv_channels:
                    self.set_channel(self.adv_channel_to_physical(channel), debug=False)
                    time.sleep(interval)
        threading.Thread(target=_adv_hopping).start()
        
    def parse_ble_packet(self, buffer, incomplete_packet=None, channel=None):
        """
        Funzione per analizzare i pacchetti BLE in un buffer, gestendo i frammenti.
        :param buffer: Dati ricevuti nel buffer corrente.
        :param incomplete_packet: Eventuale pacchetto incompleto dal buffer precedente.
        :return: Lista di pacchetti completi e un eventuale pacchetto incompleto.
        """
        
        # Cerchiamo tutti i pacchetti all'interno del buffer, se rimango dati incompleti li restituiamo
        # Per trovare i pacchetti controlliamo se c'è il preambolo e se la lunghezza del pacchetto è corretta
        packets = []
        start_index = 0
        buffer = incomplete_packet + buffer if incomplete_packet is not None else buffer
        
        if len(buffer) == 0:
            return [], None
        
        while start_index < len(buffer):
            if buffer[start_index] == BLE_PREAMBLE:
                # Skip preamble
                packet_start = start_index
                start_index += 1 # skip preamble
                
                # Check if there are enough bytes to read the access address
                if len(buffer[start_index:]) < 4:
                    return packets, buffer[packet_start:]
                
                access_address = int.from_bytes(buffer[start_index:start_index+4], byteorder='little')
                start_index += 4 # skip access address
                
                whitening_channel = self.get_physical_channel(channel) if channel is not None else self.get_physical_channel(self.ble_channel)
                
                try:
                    if access_address == BLE_ACCESS_ADDR_ADV:
                        packet_header = dewhitening(buffer[start_index:start_index+2], whitening_channel)
                        packet_length = packet_header[1] & 0x3f
                    else:
                        packet_header = dewhitening(buffer[start_index:start_index+2], whitening_channel)
                        packet_length = packet_header[1]
                except Exception as e:
                    continue
                
                # Se non ci sono abbastanza byte per leggere il pacchetto, restituisci i dati rimanenti
                if (2 + packet_length + 3) > len(buffer[start_index:]):
                    return packets, buffer[packet_start:]
                
                packet_data = dewhitening(buffer[start_index:start_index+packet_length+3+2], whitening_channel)
                
                if self.crcEnabled:
                    crc_data = crc(packet_data[:-3], packet_length + 2, self.crcInit)
                    if crc_data != packet_data[-3:]:
                        start_index += 1
                        continue
                
                packets.append(access_address.to_bytes(4, 'little') + bytes(packet_data))
                
            else:
                start_index += 1
        
        return packets, None
    
    def process_packet(self, packet, channel):
        scapy_packet = BTLE(packet)
        self.total_packets += 1
        self.packet_queue.put(scapy_packet)

    def sniff(self):
        def _sniff():
            incomplete_packets = [None] * 10  # Un pacchetto incompleto per ogni canale del channelizer
            
            while True:
                channel_data = self.get_data()
                
                for data, ble_channel in channel_data:
                    if not data:
                        continue
                    
                    #print(f"Channel {self.get_physical_channel(ble_channel)} - {len(data)} bytes")
                    packets, incomplete_packets[ble_channel] = self.parse_ble_packet(
                        data, 
                        incomplete_packets[ble_channel], 
                        ble_channel  # Passa il canale al parser
                    )
                    
                    for p in packets:
                        self.process_packet(p, self.get_physical_channel(ble_channel))
        
        threading.Thread(target=_sniff).start()
            
    def get_packets(self) -> list:
        # Recupera i pacchetti dalla coda
        packets = []
        while not self.packet_queue.empty():
            packets.append(self.packet_queue.get())
        return packets
    
    def feed_wiresharsk(self, ip='127.0.0.1', port=5555):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while True:
            # Recupera pacchetti dalla coda
            packet = self.packet_queue.get()
            if packet is None:  # Segnale per terminare il thread
                break
            self.sock.sendto(bytes(packet), (ip, port))
        self.sock.close()
    
    def exit(self):
        self.packet_queue.queue.clear()
        self.stop()

