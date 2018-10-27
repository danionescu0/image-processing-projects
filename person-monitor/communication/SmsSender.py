import requests
import urllib


class SmsSender:
    def __init__(self, url: str) -> None:
        self.__url = url

    def send(self, text: str) -> bool:
        say_url = self.__url + '&' + urllib.parse.urlencode({'msg' : text})
        try:
            requests.get(say_url, timeout = 1)
        except Exception:
            print ("error")
            return False

        return True