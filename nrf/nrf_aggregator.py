""" aggregator.py
    ####
"""
import queue
import socket
import time

from scapy.contrib.nrf_sniffer import *
from SnifferAPI import Sniffer, UART, Types, Pcap
from numpy import array_split
from threading import Thread
import logging

class NRFSniffersAggregator():
    def __init__(self, port_list: list, adv_channels=[37, 38, 39]):
        if port_list is None or len(port_list) < 1:
            raise Exception('port_list is either empty or None')
        self.ports = port_list
        self.adv_channels = adv_channels
        self.sniffers = []
        self.channel_sniffer_map = {}
        self.packet_queue = queue.Queue()
        self.threads_ojects = []
        self.running = False
        self.sniffer_adv_channels = []
        
    def _assign_channels(self):
        adv_channels = array_split(self.adv_channels, len(self.ports))
        for i, s in enumerate(self.sniffers):
            self.sniffer_adv_channels.append(adv_channels.pop().tolist())

    def setup(self):
        for p in self.ports:
            self.sniffers.append(Sniffer.Sniffer(portnum=p, baudrate=1000000, debug=False))
            
        self._assign_channels()
        
        for i, s in enumerate(self.sniffers):
            s.totalPackets = 0
            print(self.sniffer_adv_channels[i])
            s.setAdvHopSequence(self.sniffer_adv_channels[i])
            s.setSupportedProtocolVersion(Types.PROTOVER_V3)
            s.start()
    
    def get_sniffers(self):
        return self.sniffers
    
    def get_packets(self):
        packets = []
        while not self.packet_queue.empty():
            packets.append(self.packet_queue.get())
        return packets
    
    def _loop(self, sniffer):
        while True:
            if self.running == False:
                break
            packets = sniffer.getPackets()
            for p in packets:
                self.packet_queue.put(p)
                sniffer.totalPackets += 1
                
            time.sleep(0.1)
    
    def run(self):
        self.running = True
        for sniffer in self.sniffers:
            t = Thread(target=self._loop, args=(sniffer,))
            t.start()
            self.threads_ojects.append(t)
            
        self.print_stats()
    
    def quit(self):
        self.running = False
        for s in self.sniffers:
            s.doExit()
    
    def print_stats(self):
        def print_job(self):
            for i, s in enumerate(self.sniffers):
                logging.INFO(f"Sniffer '{s.portnum}' [{self.sniffer_adv_channels[i]}] - Total packets: {s.totalPackets}")
            time.sleep(5)
        t = Thread(target=print_job, args=())
        t.start()
        t.join()
        
    
    def feed_wireshark(self, ip="127.0.0.1", port=5555):
        def _wireshark(self):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while True:
                # Recupera pacchetti dalla coda
                if self.running is False:
                    break
                packet = self.packet_queue.get()
                if packet is None:  # Segnale per terminare il thread
                    continue
                self.sock.sendto(bytes(packet.getList()), (ip, port))
            self.sock.close()
        t = Thread(target=_wireshark, args=(self,))
        t.start()