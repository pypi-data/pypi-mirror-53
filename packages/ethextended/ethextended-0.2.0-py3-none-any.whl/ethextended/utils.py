from sha3 import keccak_256
from .errors import *

class Utils:
    def clear_0x(hex):
        if hex[:2] == "0x":
            return hex[2:]
        else:
            return hex

    def is_hex(text):
        text = Utils.clear_0x(text)
        try:
            for i in range(0, len(text)):
                number = int(text[i], 16)
            return True
        except:
            return False

    def is_address(addr):
        addr = Utils.clear_0x(addr)
        if len(addr) != 40:
            return False
        return Utils.is_hex(addr)



    def to_checksum_address(addr):
        addr = Utils.clear_0x(addr)
        checksum_addr = ""
        if Utils.is_address(addr):
            addr_hash = keccak_256(bytes(addr.lower(), "utf-8")).hexdigest()
            for i in range(0, 40):
                if int(addr_hash[i], 16) > 7:
                    checksum_addr += addr[i].upper()
                else:
                    checksum_addr += addr[i].lower()
        else:
            raise(InvalidAddress)

        return "0x" + checksum_addr
