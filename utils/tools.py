#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Mini_Spotify
@File    ：tools.py
@Author  ：Ruiyang Chen
"""

import time


# Log a request
def log_request(request_data, host, host_port, client_ip, client_port):
    with open("request_log.txt", "a") as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        method = request_data.get("method", "UNKNOWN")
        url = request_data.get("url", "/")
        version = request_data.get("version", "HTTP/1.1")

        headers = f"Host:  {host}:{host_port}\n"
        headers += f"Client IP: {client_ip}, Client Port: {client_port}\n"

        file.write(f"{timestamp} - {method} {url} {version}\n")
        file.write(headers)
        file.write(f"Request Body: {request_data}\n")
        file.write("\n")


# Log a response
def log_response(response_data, status, client_ip, client_port):
    with open("response_log.txt", "a") as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        version = "HTTP/1.1"

        file.write(f"{timestamp} - {version} {status}\n")
        file.write(f"Client IP: {client_ip}, Client Port: {client_port}\n")
        file.write(f"Response Body: {response_data}\n")
        file.write("\n")
