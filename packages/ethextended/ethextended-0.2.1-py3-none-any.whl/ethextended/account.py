import requests
import json
from bs4 import BeautifulSoup
from .utils import Utils as utils
from .errors import *


search_endpoint = "https://etherscan.io/searchHandler"
address_page_endpoint = "https://etherscan.io/address/"
etherscan_api_endpoint = "https://api.etherscan.io/api"

class Account:

    def address_autocomplete(address):
        address = utils.clear_0x(address)
        if not utils.is_hex(address):
            raise(InvalidAddress)
        api_request = requests.get(search_endpoint + "?term=0x{0}".format(address)).text.replace("\\t", "")
        addresses_raw = json.loads(api_request)
        addresses = []
        for address in addresses_raw:
            if len(address) >= 42:
                addresses.append(utils.to_checksum_address(address[:42]))
        return addresses



    def address_tags(addr):
        if not utils.is_address(addr):
            raise(InvalidAddress)
        address = utils.to_checksum_address(addr)
        etherscan_page = requests.get(address_page_endpoint + address).text
        etherscan_page = BeautifulSoup(etherscan_page, features="lxml")
        tags = etherscan_page.find_all("div", {"class": "mt-1"})[1].get_text()
        tags = tags.replace("\n", "")
        tags = tags.split("\xa0")
        tags_finalized = []
        for tag in tags:
            if tag != "":
                if tag[-1] == " ":
                    tag = tag[:-1]
                tags_finalized.append(tag)
        return tags_finalized

    def address_label(addr):
        if not utils.is_address(addr):
            raise (InvalidAddress)
        address = utils.to_checksum_address(addr)
        etherscan_page = requests.get(address_page_endpoint + address).text
        etherscan_page = BeautifulSoup(etherscan_page, features="lxml")
        label = etherscan_page.find("span", {"title": "Public Name Tag (viewable by anyone)"})
        if not label:
            return ""
        label = label.get_text()
        label_list = list(label)
        label_list.reverse()
        x = 0
        while label_list[0] == " ":
            label_list = label_list[1:]
        label_list.reverse()
        label = "".join(label_list)
        return label

    def transactions(addr):
        if not utils.is_address(addr):
            raise(InvalidAddress)

        address = utils.to_checksum_address(addr)
        etherscan_api_request = requests.get(etherscan_api_endpoint + "?module=account&action=txlist&address={0}&sort=desc".format(address))
        transaction_list = etherscan_api_request.json()["result"]
        return transaction_list