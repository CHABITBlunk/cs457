# network layer - data plane

### intro

- layer 3 problem
  - how do we build networks of global scale by interconnecting different types of smaller networks?
    - internetworking
  - main functions: forwarding & routing
    - divided into data plane problem & control place problem
- network layer (strictly speaking) doesn't solve problem of connecting multiple hosts in smaller networks
  - layer 2 problem
  - we assume they're connected

### toc

- overview
  - data plane
  - control plane
- what's inside a router
  - i/o ports, switching
  - buffer mgmt
  - scheduling
- ip
  - datagram format, addressing
  - network addr translation (nat)
  - ipv6
- generalized forwarding
  - match & action
  - openflow
  - middleboxes
- internet architecture

## overview

### services & protocols

- transport segment from sending to receiving host
  - sender: encapsulates segments into datagrams, passes to link layer
  - receiver: delivers segments to transport layer protocol
- network layer protocols in every internet device: hosts, routers
- routers
  - examine header fields in all ip datagrams passing through it
  - moves datagrams from input ports to output ports to transfer datagrams along e2e path

### internetworking

- what is ip
  - internet protocol
  - key tool used today to build scalable, heterogeneous internetworks
  - runs on all nodes in a collection of networks & defines the infrastructure that allows these nodes & networks to function as a single logical internetwork

### key network layer functions

- forwarding: move pkts from a router's input link to appropriate router output link
  - getting through single interchange
- routing: determine route taken by pkts from source to destination - routing algorithms
  - planning trip from source to destination

### network layer: data plane, control plane

- data plane
  - local, per-router function
  - determines how datagram arriving on router input port is forwarded to router output port
- control plane
  - network wide logic
  - determines how datagram is routed among routers along e2e path from source to destination
  - 2 approaches
    - traditional routing algorithm: implemented in routers
    - software-defined networking (sdn): implemented in remote servers

### per-router control plane

- individual routing algorithm components in each & every router interact in control plane

### sdn control plane

- remote controller computes & installs forwarding tables in routers

### network service model

- what service model for "channel" transporting datagrams from sender to receiver?
  - individual datagram example
    - guaranteed delivery with less than 40 ms delay
  - flow of datagrams example
    - in-order delivery
    - guaranteed min bandwidth to flow
    - restrictions on changes in inter pkt spacing
- best effort service model
  - no guarantees on
    - successful datagram delivery to destination
    - timing or order of delivery
    - bandwidth available to e2e flow
  - simplicity of mechanism allows internet to be widely deployed & adopted
  - sufficient provisioning of bandwidth allows performance of real time apps to be good enough most of the time
  - replicated, app layer distributed services connecting close to clients' networks, allow services to be provided from multiple locations
  - congestion control of elastic services helps

## what's inside a router

### high level view

- routing, mgmt control plane (software) operates in ms time frame
- forwarding data plane (hardware) operates in ns time frame

### input port functions

- physical layer: bit level reception
- link layer: e.g. ethernet
- decentralized switching
  - using header field values, look up output port using forwarding table in input port memory (match plus action)
  - goal: complete input port processing at line speed
  - input port queuing: if datagrams arrive faster than forwarding rate into switch fabric
  - destination based forwarding: forward based only on destination ip (traditional)
  - generalized forwarding: forward based on any set of header field values

### switching fabrics

- transfer pkt from input link to appropriate output link
- switching rate: rate at which pkts can be transferred from inputs to outputs
  - often measured as multiple of i/o line rate
  - n inputs: switching rate n times line rate desirable
- 3 major types of switching fabrics
  - memory
  - bus
  - interconnection network

### switching via memory

- 1st gen routers
  - traditional computers with switching under direct control of cpu
  - pkt copied to system mem
  - speed limited by mem bandwidth (2 bus crossings per datagram)

### switching via bus

- datagram from input port mem to output port mem via shared bus
- bus contention: switching speed limited by bus bandwidth
- 32 Gbps bus, cisco 5600: sufficient speed for access routers

### switching via interconnection network

- crossbar, clos networks, other interconnection nets initially developed to connect processors in multiprocessor
- multistage switch: n x n switch from multiple stages of smaller switches
- exploiting parallelism
  - fragment datagram into fixed length cells on entry
  - switch cells through fabric, reassemble datagram at exit
- scaling, using multiple switching planes in parallel
  - speedup, scaleup via parallelism
- cisco crs router
  - basic unit: 8 switching planes
  - each plane: 3 stage interconnection network
  - up to 100s Tbps switching capacity

### input port queuing

- if switch fabric slower than input ports combined -> queuing may occur at input queues
  - queuing delay & loss due to input buffer overflow
- head of line (hol) blocking: queued datagram at front of queue prevents others in queue from moving forward

### output port queuing

- buffering required when datagrams arrive from fabric faster than link transmission rate
- which datagrams to drop if no free buffers?
- scheduling discipline chooses among queued datagrams for transmission
  - priority scheduling - who gets best performance, network neutrality
- buffering when arrival rate via switch exceeds output line speed
- queuing delay & loss due to output port buffer overflow

### how much buffering

- rfc 3439 rule of thumb: avg buffering equal to typical $rtt * link capacity$
- more recent recommendation: with n flows, buffering = $rtt * c / sqrt(n)$
- too much buffering can increase delays (esp in home routers)
  - long rtts: poor performance for real time apps, sluggish tcp response
  - keep bottleneck link busy but not congested

### buffer mgmt

- drop: which pkt to add or drop when buffers are full
  - tail drop: drop arriving pkt
  - priority: drop/remove on priority basis
- marking: which pkts to mark to signal congestion (ecn, red)

### pkt scheduling

- decide which pkt to send next on link
  - fcfs
    - transmit pkts in order of arrival to output port
  - priority
    - arriving traffic classified, queued by class
      - any header fields can be used for classification
    - send pkt from highest priority queue that has buffered pkts
      - fcfs within priority class
  - round robin
    - arriving traffic classified, queued by class
      - any header fields can be used for classification
    - server cyclically, repeatedly scans class queues, sending 1 complete pkt from each class (if available) in turn
  - weighted fair queuing
    - generalized round robin
    - each class i has weight w, gets weighted amount of service in each cycle: $w_i / \displaystyle\sum_{j} w_j$
    - min bandwidth guarantee per traffic class

### network neutrality

- how an isp should share/allocate resources
  - pkt scheduling, buffer mgmt are mechanisms
- social, economic principles
  - protecting free speech
  - encouraging innovation & competition
- enforced legal rules & policies
- 2015 us fcc order on protecting & promoting an open internet
  - no blocking
  - no throttling
  - no paid prioritization
- 2017: rollback of 2015 order
- 2024: rollback of 2017 rollback

### isp: telecomms or info service?

- us telecomm act of 1934 & 1936
  - title ii: imposes common carrier duties on telecomms services: reasonable rates, non discrimination, requires regulation
  - title i: applies to info services
    - no common carrier duties (not regulated)
    - grans fcc authority "as may be necessary in the execution of its functions"

### ip datagram forwarding

- strat
  - every datagram contains dest addr
  - if directly connected to dest network, forward to host
  - if not directly connected to dest network, forward to same router
  - forwarding table maps network number into next hop
  - each host has default router
  - each router maintains forwarding table
- algorithm
  - if network num of dest = network num of interface, deliver pkt to dest over that interface
  - else if dest network num in forwarding table, deliver to nexthop router
  - else deliver pkt to default router
