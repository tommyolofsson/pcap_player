#!/usr/bin/env python

import argparse
import pcapfile.savefile
import socket
import time


def _packet_ts(packet):
    return packet.timestamp + 1e-6 * packet.timestamp_ms


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('pcap', nargs='+', help="Path to pcap file(s)")
    ap.add_argument('--itf', default='eth0', help="Interface to replay on.")
    ap.add_argument('--Kt', type=float, default=1.0,
                    help="Time factor (higher is faster).")
    args = ap.parse_args(argv)

    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)

    for pcap_path in args.pcap:
        with open(pcap_path, 'r') as pcap_file:
            print "Loading %s..." % pcap_path
            pcap = pcapfile.savefile.load_savefile(pcap_file)

            n = len(pcap.packets)
            t = _packet_ts(pcap.packets[-1]) - _packet_ts(pcap.packets[0])
            print "Replaying %d packets during %f seconds..."  % (n, t)

            t0_pcap = _packet_ts(pcap.packets[0])
            t0_sys = time.clock()
            for packet in pcap.packets:
                t_send_pcap = _packet_ts(packet)
                t_send_pcap_rel = t_send_pcap - t0_pcap
                t_send_sys_rel = args.Kt * t_send_pcap_rel
                t_send_sys = t_send_sys_rel + t0_sys
                while True:
                    delay = t_send_sys - time.clock()
                    if delay <= 0:
                        break
                    time.sleep(delay)
                sock.sendto(packet.raw(), (args.itf, 0, 0))


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
