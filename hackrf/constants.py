BLE_PREAMBLE = int.from_bytes(b'\xaa', byteorder='big')
BLE_ACL_PREAMBLE = int.from_bytes(b'\x55', byteorder='big')
BLE_ACCESS_ADDR_ADV = 0x8e89bed6
BLE_ADDR_LEN = 4