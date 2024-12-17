def swap_bits(value):
    return (value * 0x0202020202 & 0x010884422010) % 1023

def crc(data, length, init=0x555555):
    ret = [(init >> 16) & 0xff, (init >> 8) & 0xff, init & 0xff]

    for d in data[:length]:
        for v in range(8):
            t = (ret[0] >> 7) & 1

            ret[0] <<= 1
            if ret[1] & 0x80:
                ret[0] |= 1

            ret[1] <<= 1
            if ret[2] & 0x80:
                ret[1] |= 1

            ret[2] <<= 1

            if d & 1 != t:
                ret[2] ^= 0x5b
                ret[1] ^= 0x06

            d >>= 1

    ret[0] = swap_bits((ret[0] & 0xFF))
    ret[1] = swap_bits((ret[1] & 0xFF))
    ret[2] = swap_bits((ret[2] & 0xFF))

    return ret

def dewhitening(data, channel):
    ret = []
    
    if channel == 0: channel = 37
    elif channel == 12: channel = 38
    
    lfsr = swap_bits(channel) | 2
    
    

    for d in data:
        d = swap_bits(d)
        for i in 128, 64, 32, 16, 8, 4, 2, 1:
            if lfsr & 0x80:
                lfsr ^= 0x11
                d ^= i

            lfsr <<= 1
            i >>= 1
        ret.append(swap_bits(d))

    return ret

# Funzione per calcolare il CRC per i pacchetti BLE
def calculate_ble_crc(data, crc_init=0x555555):
    crc_poly = 0x00065B
    crc = crc_init

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x000001:
                crc = (crc >> 1) ^ crc_poly
            else:
                crc >>= 1

    return [(crc >> i) & 0xFF for i in (0, 8, 16)]