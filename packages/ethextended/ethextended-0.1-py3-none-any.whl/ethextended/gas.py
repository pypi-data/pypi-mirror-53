import requests

ethgasstation_endpoint = "https://ethgasstation.info/json/ethgasAPI.json"

class Gas:
    @staticmethod
    def fast_wei():
        api_request = requests.get(ethgasstation_endpoint).json()
        return int(api_request["fast"] / 10 * 1000000000)

    @staticmethod
    def fast_waittime():
        api_request = requests.get(ethgasstation_endpoint).json()
        return api_request["fastWait"] * 60

    @staticmethod
    def avg_wei():
        api_request = requests.get(ethgasstation_endpoint).json()
        return int(api_request["average"] / 10 * 1000000000)

    @staticmethod
    def avg_waittime():
        api_request = requests.get(ethgasstation_endpoint).json()
        return api_request["avgWait"] * 60

    @staticmethod
    def slow_wei():
        api_request = requests.get(ethgasstation_endpoint).json()
        return int(api_request["safeLow"] / 10 * 1000000000)

    @staticmethod
    def slow_waittime():
        api_request = requests.get(ethgasstation_endpoint).json()
        return api_request["safeLowWait"] * 60