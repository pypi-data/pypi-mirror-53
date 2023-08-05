# -*- coding: utf-8 -*-
import sys
import http.client
import os

class Discord_msg():
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, msg):
        formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + msg + "\r\n------:::BOUNDARY:::--"

        connection = http.client.HTTPSConnection("discordapp.com")
        connection.request("POST", self.webhook_url, formdata.encode('utf-8'), {
            'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
            'cache-control': "no-cache"
            })
        response = connection.getresponse()
        result = response.read()
        return(result.decode("utf-8"))

if __name__ == '__main__':
    pass