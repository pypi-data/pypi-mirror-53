import requests
import string
from .account import InvalidAddress, verify_address
import base64

# Using https://eth.vanity.show
identicon_endpoint = "https://eth.vanity.show/"

class Identicon:
    def base64(addr):
        address = verify_address(addr)
        hexcheck = all(c in string.hexdigits for c in address[2:])
        if not (hexcheck and len(address) == 42):
            print(len(address))
            print(hexcheck)
            raise(InvalidAddress)

        image_bytes = requests.get(identicon_endpoint + address).content
        return base64.b64encode(image_bytes)

    def url(addr):
        address = verify_address(addr)
        return identicon_endpoint + address