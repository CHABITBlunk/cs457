# chapter 3

### toc
- transport layer
- multiplexing & demultiplexing
- udp
- principles of reliable data transfer
- bandwidth & delay
- tcp
- principles of congestion control
- tcp congestion control
- evolution of tls

## transport layer

### transport services & protocols
- provide logical comms between app procs running on different hosts
- transport protocol actions in end systems
  - sender: breaks app messages into segments, passes to network layer
  - receiver: reassembles segments into messages, passes to application layer

### transport vs network layer services & protocols
- transport: comms between procs
  - relies on, enhances network layer services
- network: comms between hosts

## multiplexing & demultiplexing

### multiplexing/demultiplexing
- multiplexing as sender
  - handle data from multiple sockets, add transport header (later used for demultiplexing)
- demultiplexing as receiver
  - use header info to deliver received segments to correct socket
- how demultiplexing works
  - host receives ip datagrams
    - each datagram has source & destination ip

### connectionless demultiplexing
- when creating socket, must specify host-local port number
- when creating datagram to send to udp socket, must specify destination ip & destination port
- when receiving host receives udp segment, checks destination port number in segment, directs udp segment to socket with that port number
- ip/udp datagrams with same destination port but different source ips and/or source ports will be directed to same socket at receiving host
- uses only destination port

### connection-oriented demultiplexing
- tcp socket identified by 4-tuple
  - source ip
  - source port
  - dest ip
  - dest port
- demux: receiver uses all 4 values to direct segment to appropriate socket

## udp

### udp
- no frills, bare bones internet transport protocol
- best effort service, udp segments may be lost or delivered out of order
- connectionless
  - no handshake between udp sender & receiver
  - each udp segment handled independently of others
- why it exists
  - no connection establishment (avoid rtt delay)
  - simple: no conn state at sender or receiver
  - small header size
  - no congestion control
    - can keep throwing pkts out as fast as desired
    - can function in the face of congestion
- use cases
  - streaming multimedia apps (loss tolerant, rate senstive)
  - dns
  - snmp
  - http/3
- if reliable transfer needed over udp (e.g. http/3)
  - add needed reliability at app layer
  - add congestion control at app layer
- udp also contains a checksum in header that receiver has to check to ensure network is good

### internet checksum
- detect errors in transmitted segment
- sender
  - treat contents of udp segment (including udp header fields & ips) as sequence of 16-bit ints
  - checksum: one's complement sum of segment content
  - checksum value put into udp checksum field
- receiver
  - compute checksum of received segment
  - check if computed checksum = checksum field value
    - not equal -> error
    - equal -> no apparent error, but maybe errors nonetheless?

## bandwidth & delay

### delay * bandwidth

- think of channel between pair of procs as hollow pipe
  - latency (delay) - length of pipe
  - bandwidth - width of pipe
- delay 50 ms, bandwidth 45 Mbps
  - 50e-3 seconds * 45e6 bits/second
  - 2.25e6 = 280 KB data

### bandwidth-delay product
- very important consideration in network design
- determines how much data can actually be transmitted

### bandwidth-delay product & performance
- latency = propagation + transmit + queue + processing
- propagation = distance/speed
- transmit = size/bandwidth
- one bit transmission - propagation is important
- large byte transmission -  bandwidth is important

### bandwidth * delay
- relative importance of bandwidth & latency depends on app
- tells us how many bits sender must transmit before first bit arrives at receiver if sender keeps pipe full
- takes another one-way latency to receive response
- sender doesn't fill pipe -> send whole delay * bandwidth product's worth of data before it stops to wait for a signal - sender will not fully utilize network

### reliable transmission
- checksum used to detect errors
  - some error codes strong enough to correct errors
  - overhead typically too high
- corrupt frames must be discarded
- transport layer protocol that wants to deliver segments reliably must recover from discarded segments
- accomplished using a combination of acknowledgements & timeouts

### ack frame
- small control segment (i.e. header only) that protocol sends back to peer saying it received an earlier segment
- receipt of ack tells sender that its segment was successfully delivered
- if sender doesn't receive ack within timeout, will re-send frame
- ack & timeouts called automatic repeat request (arq)

### stop & wait protocol
- after transmitting one segment, sender waits for ack
- if ack not received after certain amount of time, segment sent again

## principles of reliable data transfer

### principles of reliable data transfer
- complexity of reliable data transfer protocol depends strongly on characteristics of unreliable channels (lose, corrupt, reorder data)
- sender & receiver don't know each other's state unless communicated via a message

### reliable data transfer protocol (rdt): interfaces
- rdt_send(): called from above, passes data to deliver to receiver upper layer
- udt_send(): called by rdt to transfer pkt over unreliable channel to receiver
- deliver_data(): called by rdt to deliver data to upper layer
- rdt_rcv(): called when pkt arrives on receiver side of channel

### getting started
- incrementally develop sender & receiver sides of rdt
- consider only unidirectional data transfer, but control info will flow in both directions
- use finite state machines (fsm) to specify sender & receiver

### rdt 1.0: reliable transfer over reliable channel
- underlying channel perfectly reliable
  - no bit errors
  - no pkt loss
- separate fsms for sender & receiver
  - sender sends data into underlying channel
  - receiver reads data from underlying channel
  
### rdt 2.0: channel with bit errors
- underlying channel may flip bits in pkt
  - checksum to detect bit errors
- how to recover from errors?
  - ack: receiver tells sender pkt received ok
  - nak: receiver tells sender pkt had errors
  - sender retransmits pkt on receipt of nak
- stop & wait!
- what happens if ack/nak corrupted?
  - sender doesn't know what happened at receiver
  - can't just retransmit: possible duplicate
- handling duplicates
  - sender retransmits current pkt if ack/nak corrupted
  - sender adds sequence number to each pkt
  - receiver discards duplicates

### rdt2.1: handling garbled ack/nak
- sender
  - sends pkt with sequence number (0, 1 will suffice), waits for ack/nak
  - if corrupted, re-send
  - if ack, keep sending
  - if nak, re-send pkt
- receiver
  - receives pkt with sequence number
  - check if pkt is duplicate
  - if pkt not corrupt, send ack
  - if pkt corrupt, send nak
  - wait for more data from sender

### rdt2.2: nak-free
- same functionality as rdt2.1, only using acks
- instead of ack, receiver sends ack for last pkt received ok
  - receiver must include seq number of pkt being acked
- duplicate ack at sender results in same action as nak: retransmit current pkt
- tcp uses rdt2.2 to be nak-free

### rdt3.0: channels with errors & loss
- channel can also lose pkts
  - checksum, sequence numbers, acks, retransmissions will be of help, but not quite enough
- sender waits reasonable amount of time for ack
  - retransmits if no ack received in time
  - if pkt or ack just delayed (not lost)
    - retransmission will be duplicate, but seq already handles this
    - receiver must specify seq of packet being acked
  - use countdown timer to interrupt after reasonable amount of time
- performance
  - usender: utilization - fraction of time sender busy sending
  - e.g.: 1 Gbps link, 15 ms dprop, 8000 bit packet - D = L/R = 8000 bits/10e9 b/s = 8 microseconds
