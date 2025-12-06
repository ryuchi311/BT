#!/usr/bin/env python3
"""Simple TCP forwarder: listens on IPv4 and forwards to an IPv6 destination.
Usage: python scripts/ipv6_proxy.py --listen 0.0.0.0 --listen-port 5433 --target db.gqk... --target-port 5432
"""
import argparse
import socket
import threading
import sys


def forward(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except Exception:
        pass
    finally:
        try:
            src.shutdown(socket.SHUT_RD)
        except Exception:
            pass


def handle_client(client_sock, target_host, target_port):
    try:
        # Resolve target host to IPv6 addresses
        infos = socket.getaddrinfo(target_host, target_port, socket.AF_INET6, socket.SOCK_STREAM)
        if not infos:
            print('No IPv6 address found for', target_host)
            client_sock.close()
            return
        af, socktype, proto, canonname, sockaddr = infos[0]
        target_sock = socket.socket(af, socktype, proto)
        target_sock.settimeout(10)
        target_sock.connect(sockaddr)
    except Exception as e:
        print('Failed to connect to target', target_host, target_port, e)
        client_sock.close()
        return

    # Start forwarding in both directions
    t1 = threading.Thread(target=forward, args=(client_sock, target_sock), daemon=True)
    t2 = threading.Thread(target=forward, args=(target_sock, client_sock), daemon=True)
    t1.start(); t2.start()
    t1.join(); t2.join()
    client_sock.close(); target_sock.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--listen', default='0.0.0.0')
    p.add_argument('--listen-port', type=int, default=5433)
    p.add_argument('--target', required=True)
    p.add_argument('--target-port', type=int, default=5432)
    args = p.parse_args()

    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((args.listen, args.listen_port))
    listen_sock.listen(5)
    print(f'Listening on {args.listen}:{args.listen_port}, forwarding to {args.target}:{args.target_port} (IPv6)')

    try:
        while True:
            client, addr = listen_sock.accept()
            thr = threading.Thread(target=handle_client, args=(client, args.target, args.target_port), daemon=True)
            thr.start()
    except KeyboardInterrupt:
        print('Stopping proxy')
    finally:
        listen_sock.close()

if __name__ == '__main__':
    main()
