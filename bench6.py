import socket
from taipanstack.security.guards import _check_ip_safety
from result import Ok, Err

def check_ip_safety_opt(hostname: str) -> Ok | Err:
    try:
        # Use simple gethostbyname if it's an IPv4 check to speed up? Actually getaddrinfo is correct for IPv6 and IPv4.
        addr_infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return Err("Hostname could not be resolved")

    import ipaddress
    # optimize ip address checking by caching the ipaddress parser
    for addr_info in addr_infos:
        raw_ip = addr_info[4][0]
        try:
            addr = ipaddress.ip_address(raw_ip)
        except ValueError:
            continue

        if (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        ):
            return Err("SSRF detected")

    return Ok(None)

import timeit
from unittest.mock import patch
public_ip = [(socket.AF_INET, socket.SOCK_STREAM, 0, "", ("93.184.216.34", 80))]

with patch("socket.getaddrinfo", return_value=public_ip):
    print(timeit.timeit(lambda: _check_ip_safety("example.com"), number=10000))
    print(timeit.timeit(lambda: check_ip_safety_opt("example.com"), number=10000))
