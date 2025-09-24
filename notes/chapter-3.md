# chapter 3

### toc
- transport layer
- multiplexing & demultiplexing
- protocols

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

## protocols

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
    - can keep throwing packets out as fast as desired
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
