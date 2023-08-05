import requests
import string
from .account import InvalidAddress
import base64
from .utils import Utils as utils

# Using https://eth.vanity.show
identicon_endpoint = "https://eth.vanity.show/"

class Identicon:
    def base64(addr):
        checksum_addr = utils.to_checksum_address(addr)
        image_bytes = requests.get(identicon_endpoint + checksum_addr).content
        return base64.b64encode(image_bytes)

    def url(addr):
        address = utils.to_checksum_address(addr)
        return identicon_endpoint + address