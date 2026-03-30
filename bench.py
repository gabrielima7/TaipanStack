from taipanstack.security.guards import _check_ip_safety
import socket
from unittest.mock import patch
import timeit
import cProfile

public_ip = [(socket.AF_INET, socket.SOCK_STREAM, 0, "", ("93.184.216.34", 80))]

with patch("taipanstack.security.guards.socket.getaddrinfo", return_value=public_ip):
    cProfile.run("[_check_ip_safety('example.com') for _ in range(100000)]", sort='tottime')
