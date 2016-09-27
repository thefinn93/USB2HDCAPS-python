#!/usr/bin/env python3
"""Sends the packets to get a StarTech.com USB2HDCAPS HDMI capture device to start streaming."""
import socket
import logging
import argparse

PORT = 8086


def find_device():
    """Find a compatible HDMI capture device on the LAN and return it's IP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 0))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(1)

    source_device = None

    while source_device is None:
        logging.debug("Searching for USB2HDCAPS device...")
        s.sendto(b"HS602", ('<broadcast>', PORT))   # Send this until it replies with a "YES" packet
        try:
            response, source = s.recvfrom(3)
            source_device = source[0]
            if response == b"YES":
                logging.info("Found device at %s" % source_device)
        except socket.timeout:
            pass
    return source_device

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interface with a USB2HDCAPS device.')

    parser.add_argument('--verbose', '-v', action='count')

    subparsers = parser.add_subparsers(help='Action')
    subparsers.required = True
    subparsers.dest = 'action'
    scan_parser = subparsers.add_parser('scan', help='Scan for USB2HDCAPS devices')
    scan_parser = subparsers.add_parser('start', help='Start streaming (not yet implimented)')
    scan_parser = subparsers.add_parser('stop', help='Stop streaming (not yet implimented)')
    args = parser.parse_args()

    if args.verbose is not None:
        logging.basicConfig(level=(4-args.verbose)*10)

    if args.action in ["stop", "start"]:
        print("Not yet implimented")
    elif args.action == "scan":
        find_device()
