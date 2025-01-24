<p align="center"><h1 align="center">TIROCINIO UNIMORE 23/24</h1></p>
<p align="center">
    <em>Repository ufficiale del tirocinio interno personale</em>
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
    <!-- default option, no dependency badges. -->
</p>
<br>

##  Table of Contents

- [ Overview](#overview)
- [ Features](#features)
- [ Project Structure](#project-structure)
  - [ Project Index](#project-index)
- [ Getting Started](#getting-started)
  - [ Prerequisites](#prerequisites)
  - [ Installation](#installation)
  - [ Usage](#usage)
- [ License](#license)
- [ Acknowledgments](#acknowledgments)

---

##  Overview

This project is divided into two distinct parts. The first part is an aggregator for nRF dongles that captures BLE advertising packets, allowing for real-time monitoring and analysis. The second part is a module designed to demodulate and decode any BLE packet using an HackRF device; it also includes additional sniffing capabilities to broaden the range of supported BLE data collection.

## Features

- **BLE Advertising Aggregation**: Collects and organizes BLE advertising packets from multiple nRF dongles in real-time, simplifying packet analysis. It also supports multiple output methods:
    - Wireshark (udpdump)
    - cli
- **HackRF Demodulation & Decoding**: Offers the ability to demodulate and decode any BLE packet using a HackRF device.
- **Data Layer Sniffing**: Capable of sniffing both channels type (data, advertising).
- **Extended Sniffing Capabilities**: Provides additional sniffing functions through the HackRF module, allowing for a broader range of BLE data collection.
    - **ADV Channel Hopping**

---

##  File Structure

```sh
└── tirocinio-ble-2024/
    ├── README.md
    ├── hackrf
    │   ├── __init__.py
    │   ├── constants.py
    │   ├── decoder.py
    │   ├── example.py
    │   └── utils.py
    └── nrf
        ├── SnifferAPI
        ├── __init__.py
        ├── nrf_aggregator.py
        ├── scapy_example.py
        └── wireshark_example.py
```


###  Project Index
<details open>
    <summary><b><code>TIROCINIO-BLE-2024/</code></b></summary>
    <details> <!-- nrf Submodule -->
        <summary><b>nrf</b></summary>
        <blockquote>
            <table>
            <tr>
                <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/nrf_aggregator.py'>nrf_aggregator.py</a></b></td>
                <td><code></code></td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/wireshark_example.py'>wireshark_example.py</a></b></td>
                <td><code></code></td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/scapy_example.py'>scapy_example.py</a></b></td>
                <td><code></code></td>
            </tr>
            </table>
            <details>
                <summary><b>SnifferAPI</b></summary>
                <blockquote>
                    <table>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/Filelock.py'>Filelock.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/CaptureFiles.py'>CaptureFiles.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/Packet.py'>Packet.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/Pcap.py'>Pcap.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/version.py'>version.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/Sniffer.py'>Sniffer.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/Types.py'>Types.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/SnifferCollector.py'>SnifferCollector.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/UART.py'>UART.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/Notifications.py'>Notifications.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/Devices.py'>Devices.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/Exceptions.py'>Exceptions.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    <tr>
                        <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/nrf/SnifferAPI/Logger.py'>Logger.py</a></b></td>
                        <td><code></code></td>
                    </tr>
                    </table>
                </blockquote>
            </details>
        </blockquote>
    </details>
    <details> <!-- hackrf Submodule -->
        <summary><b>hackrf</b></summary>
        <blockquote>
            <table>
            <tr>
                <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/hackrf/utils.py'>utils.py</a></b></td>
                <td><code></code></td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/hackrf/constants.py'>constants.py</a></b></td>
                <td><code></code></td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/hackrf/decoder.py'>decoder.py</a></b></td>
                <td><code></code></td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/RaY3R/tirocinio-ble-2024/blob/master/hackrf/example.py'>example.py</a></b></td>
                <td><code></code></td>
            </tr>
            </table>
        </blockquote>
    </details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with this repo, ensure your runtime environment meets the following requirements:

- Python 3.x
- Gnuradio X.x


###  Installation

Install tirocinio-ble-2024 using one of the following methods:

1. Clone the tirocinio-ble-2024 repository:
```sh
❯ git clone https://github.com/RaY3R/tirocinio-ble-2024
```

2. Navigate to the project directory:
```sh
❯ cd tirocinio-ble-2024
```

3. Install the project dependencies:

**Gnuradio**

Please refer to the official [guide](https://wiki.gnuradio.org/index.php/InstallingGR#Quick_Start)



###  Usage
Navigate each directory and run the example files.

```sh
❯ python3 nrf/scapy_example.py
```

---

##  License

This project is protected under the GPLv3 License. 

---

##  Acknowledgments

- [Rtone's sdr4iot BLE repository](https://github.com/Rtone/sdr4iot-ble-rx)
- [Scapy nrf module](https://scapy.readthedocs.io/en/latest/)

