import os
import random
from dotenv import load_dotenv

load_dotenv()

# Proxy and Headers Configuration
def get_proxy():
    host, port = os.environ.get('PROXY_HOST').split(":")
    username = os.environ.get('PROXY_USERNAME')
    password = os.environ.get('PROXY_PASSWORD')
    return f'http://{username}:{password}@{host}:{port}'

def get_headers():
    HEADERS_LIST = [
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/127.0.0.0"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; U; nl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11"},
        {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; Win64; x64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; Zoom 3.6.0; wbx 1.0.0; cwms 1.0.0; Zoom 3.6.0)"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"},
        {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; ru) Presto/2.9.168 Version/11.50"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36 OPR/112.0.5197.53"}
    ]
    return random.choice(HEADERS_LIST)
