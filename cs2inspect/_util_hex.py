__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "04.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"


import struct
import zlib

from cs2inspect.econ_pb2 import CEconItemPreviewDataBlock


def float_to_bytes(float_value: float) -> int:
    float_bytes = struct.pack('>f', float_value)
    return struct.unpack('>I', float_bytes)[0]


def bytes_to_float(int_value: int) -> float:
    int_bytes = struct.pack('>I', int_value)
    return struct.unpack('>f', int_bytes)[0]


def hex_to_bytes(hex_str: str) -> bytes:
    return bytes.fromhex(hex_str)


def to_hex(data_block: CEconItemPreviewDataBlock) -> str:
    # Needs to be prefixed with a null byte
    buffer = bytearray([0])
    buffer.extend(data_block.SerializeToString())

    # calculate the checksum
    crc = zlib.crc32(buffer)
    xored_crc = (crc & 0xFFFF) ^ (data_block.ByteSize() * crc)

    buffer.extend((xored_crc & 0xFFFFFFFF).to_bytes(length=4, byteorder='big'))

    # Must be upper case
    return buffer.hex().upper()


def from_hex(hex_str: str) -> CEconItemPreviewDataBlock:
    # Convert hex string to bytes
    data_bytes = hex_to_bytes(hex_str)

    if not data_bytes:
        raise ValueError("Empty hex string")

    # If first byte is not 0, it's an XOR masked link
    if data_bytes[0] != 0:
        mask = data_bytes[0]
        data_bytes = bytes(b ^ mask for b in data_bytes)

        if data_bytes[0] != 0:
            raise ValueError("Invalid masked inspect hex payload")

    # Remove the first null byte
    data_bytes = data_bytes[1:]

    # Remove the last 4 bytes (CRC checksum)
    if len(data_bytes) >= 4:
        data_bytes = data_bytes[:-4]

    # Deserialize the protobuf message
    data_block = CEconItemPreviewDataBlock()
    data_block.ParseFromString(data_bytes)

    return data_block


if __name__ == '__main__':
    exit(1)
