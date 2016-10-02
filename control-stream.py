#!/usr/bin/env python3
"""Sends the packets to get a StarTech.com USB2HDCAPS HDMI capture device to start streaming."""
import socket
import logging
import argparse


def find_device():
    """Find a compatible HDMI capture device on the LAN and return it's IP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 0))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(1)

    source_device = None

    logging.info('Searching for USB2HDCAPS device...')

    while source_device is None:
        logging.debug("Searching for USB2HDCAPS device...")
        s.sendto(b"HS602", ('<broadcast>', 8086))   # Send this until it replies with a "YES" packet
        try:
            response, source = s.recvfrom(3)
            source_device = source[0]
            if response == b"YES":
                logging.info("Found device at %s" % source_device)
        except socket.timeout:
            pass
    return source_device


def start(host, port=8087):
    """Tell the specified device to start streaming."""
    print("Not yet implimented")
    exit(1)


def stop(host, port=8087):
    """Tell the specified device to stop streaming."""
    print("Not yet implimented")
    exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interface with a USB2HDCAPS device.')

    parser.add_argument('--verbose', '-v', action='count')

    subparsers = parser.add_subparsers(help='Action')
    subparsers.required = True
    subparsers.dest = 'action'

    scan_parser = subparsers.add_parser('scan', help='Scan for USB2HDCAPS devices')

    start_parser = subparsers.add_parser('start', help='Start streaming (not yet implimented)')
    start_parser.add_argument('--host', '-H',
                              help='The host to connect to. The first host to respond to a scan '
                                   'will be used if this is unset.')
    start_parser.add_argument('--port', '-p', help='The port to connect to.', default=8087,
                              type=int)

    stop_parser = subparsers.add_parser('stop', help='Stop streaming (not yet implimented)')
    stop_parser.add_argument('--host', '-H',
                             help='The host to connect to. The first host to respond to a scan '
                                  'will be used if this is unset.')
    stop_parser.add_argument('--port', '-p', help='The port to connect to.', default=8087,
                             type=int)

    args = parser.parse_args()

    if args.verbose is not None:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.action == "scan":
        find_device()
    elif args.action == "stop":
        host = args.host
        if host is None:
            host = find_device()
        stop(host, args.port)
    elif args.action == "start":
        host = args.host
        if host is None:
            host = find_device()
        start(host, args.port)
