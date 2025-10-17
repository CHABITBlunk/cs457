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

### destination based forwarding

- foundations of subnetting
- ranges of ip addrs that output to different interfaces, then a default or "otherwise" case
- what if i want to reserve a range inside of a range?
  - any addr inside both ranges could satisfy both, so which interface do we choose on which to send it?

### longest prefix matching

- when looking for forwarding table entry for given dest addr, use longest addr prefix that matches dest addr
- previous example: when we have more bits that are the same, follow that and send it across a more specific interface
- often performed using ternary content addressable memories (tcams)
  - content addressable: present addr to tcam: retrieve addr in one clock cycle, regardless of table size
  - cisco catalyst: ~1m routing table entries in tcam

## ip

### network layer: internet

- ip protocol
  - datagram format
  - addressing
  - pkt handling conventions
- icmp protocol
  - error reporting
  - router "signaling"
- path selection algorithms
  - implemented in
    - routing protocols (ospf, bgp)
    - sdn controller

### datagram format

- tcp pkt format built off of this, so architecture is virtually the same
- overhead - 40 bytes
  - 20 bytes of tcp
  - 20 bytes of ip

### fragmentation & reassembly

- each network has some mtu (max transmission unit)
  - ethernet (1500 bytes), fddi (4500 bytes)
- strat
  - fragmentation occurs in a router when it gets a datagram that it wants to forward over a network with lower mtu size than datagram size
  - reassembly done at receiving host
  - all fragments carry same identifier in ident field
  - fragments are self-contained datagrams
  - ip doesn't recover from missing fragments
- header fields used in ip fragmentation
  - unfragmented pkt
  - fragmented pkts

### ip addressing - intro

- ip addr: 32 bit identifier associated with each host or router interface
- interface: conn between host/router & physical link
  - routers typically have multiple interfaces
  - host typically has 1-2 interfaces

### ipv4 addr

- 32 bit number (4 B addrs)
- identifies an interface
- represented in dotted quad notation

### hierarchical addressing

- grouping related hosts
  - internet is an internetwork
    - used to connect networks together, not hosts
    - needs a way to address a network
- scalability challenge
  - suppose hosts had arbitrary addrs
    - every router would need a lot of information to know how to direct pkts toward host
- ip prefixes
  - divided into network & host portions
  - network with netmask /24 has 2^8 addrs
- scalability improved
  - number related hosts from common subnet
- easy to add new hosts
  - no need to update routers
    - adding new host doesn't require adding a new forwarding entry
- route aggregation
  - hierarchical addressing allows efficient advertisement of routing information
- more specific routes
  - different isps can advertise more specific routes

### subnets

- device interfaces that can physically reach each other without passing through an intervening router
- ip addrs have structure
  - subnet part: devices in same subnet have common high order bits
  - host part: remaining low order bits
- detach each interface from its host or router, creating islands of isolated networks

### how to get ip addr

- how does a host get an ip?
  - hard coded by sysadmin in config file (e.g. `/etc/rc.config` in unix)
  - dhcp: dynamically get addr from server (plug & play)
- how does a network get a subnet?
  - gets allocated portion of its provider isp's addr space

### ip addressing: cidr (classless interdomain routing)

- subnet portion of addr of arbitrary length
- addr format: a.b.c.d/x, where x is num bits in subnet portion of addr

### dhcp

- goal: host dynamically obtains ip from network server when it joins network
  - can renew lease on addr in use
  - allows reuse of addrs (only hold addr while connected/on)
  - support for mobile users who join/leave network
- overview
  - host broadcasts dhcp discover msg (optional)
  - dhcp server responds with dhcp offer msg (optional)
  - host requests ip addr: dhcp request
  - dhcp server sends addr: dhcp ack
- can also return
  - addr of first hop router for client
  - name & ip of dns
  - network mask (indicating network vs host portion of addr)

### nat (network addr translation)

- all devices in a lan share just one ipv4 addr as far as outside world is concerned
- all datagrams leaving lan have same source nat ip, but different source ports
- datagrams with source or dest in lan have private ip addr for source & destination
- all devices in lan have 32-bit addrs in a private ip addr space (10/8, 172.16/12, 192.168/16) that can only be used in local network
- advantages
  - just one ip addr needed from provider isp for all devices
  - can change addrs of host in local network without notifying outside world
  - can change isp without changing lan device addrs
  - security: devices inside local net not directly addressable or visible to outside world
- implementation: nat router must (transparently)
  - outgoing datagrams: replace (source ip, port) of every outgoing datagram to (nat ip, new port)
    - remote clients/servers will respond using (nat ip, new port) as dest addr
  - remember (in translation table) every ((source ip, port), (nat ip, new port)) pair
  - incoming datagrams: replace (nat ip, new port) in dest fields of every incoming datagram with corresponding (source ip, port) in nat table
- controversy
  - routers should only process up to layer 3
  - addr shortage should be solved by ipv6
  - violates e2e argument (port manipulation by network layer device)
  - nat traversal: what if client wants to connect to server behind nat?
- nat extensively used in home & institutional nets, 4g/5g cell nets

### ipv6 motivation

- initial motivation: 32 bit ipv4 addr space would be completely allocated
- additional motivation
  - speed processing/forwarding: 40 byte fixed length header
  - enable different network layer treatment of flows

### ipv6 datagram format

- compared with ipv4
  - no checksum (speed processing at routers)
  - no fragmentation/reassembly
  - no options (available at upper layer, next header protocol at router)

### transition from ipv4 to ipv6

- not all routers can be upgraded simultaneously
  - no flag days
  - how will network operate with mixed ipv4 & ipv6 routers?
- tunneling: ipv6 datagram carried as payload in ipv4 datagram among ipv4 routers (pkt within pkt)
  - tunneling used extensively in other contexts (4g/5g)

### tunneling & encapsulation

- generally done by wrapping ipv6 pkts with ipv4, since some devices support ipv6, but every device supports ipv4

### ipv6 adoption

- google: ~40% of clients access services via ipv6
- nist: 1/3 of all us govt domains are ipv6 capable
- long time for deployment & use
  - been in progress for 25 years so far
  - app level changes in the last 25 years: www, social media, streaming, etc.

## generalized forwarding

### match + action

- each router contains forwarding table (flow table)
  - match + action abstraction: match bit in arriving pkt & take action
    - destination based forwarding: forward based on dest ip
    - generalized forwarding
      - many header fields can determine action
      - many actions possible: drop/copy/modify/log pkt

### flow table abstraction

- flow: defined by header field values (in link, network, transport layer fields)
- generalized forwarding: simple pkt handling rules
  - match: pattern values in pkt header fields
  - actions: for matched pkt: drop, fwd, modify, matched pkt or send matched pkt to controller
  - priority: disambiguate overlapping patterns
  - counters: num bytes & num pkts

### openflow abstraction

- match + action: abstraction unifies different kinds of devices
  - router
    - match: longest dest ip prefix
    - action: fwd out link
  - switch
    - match: dest mac addr
    - action: fwd or flood
  - firewall
    - match: ip addr & tcp/udp ports
    - action: permit or deny
  - nat
    - match: ip addr & port
    - action: rewrite addr & port
- orchestrated tables can create network wide behavior

### generalized forwarding: summary

- match + action abstraction: match bits in arriving pkt headers in any layers & take action
  - matching over many fields (link, network, transport layer)
  - local actions: drop, fwd, mod, send matched pkt to controller
  - program network wide behaviors
- simple form of network programmability
  - programmable, per packet processing
  - historical roots: active networking
  - today: more generalized programming (https://p4.org)

### middleboxes

- any intermediary box performing functions apart from normal, standard functions of an ip router on the data path between src & dest
- examples
  - nat
    - home, cellular, institutional
  - app specific
    - service providers, institutional, cdn
  - firewalls, ids
    - corporate, institutional, service providers, isps
  - load balancers
    - corporate, service provider, data center, mobile nets
  - caches
    - service provider, mobile, cdn
- initially were proprietary (closed) hardware solutions
- move towards "whitebox" hardware implementing open api
  - move away from proprietary hardware solutions
  - programmable local actions via match + action
  - move towards innovation/differentiation in software
- sdn: (logically) centralized control & config mgmt often in private/public cloud
- network functions virtualization (nfv): programmable services over white box networking, computation, & storage

## internet architecture

### ip hourglass

- internet's thin waist
  - one network layer protocol: ip
  - must be implemented by every internet connected device
  - many protocols in physical, link, transport, & app layers
- middle age: include nfv, nat, caching, & firewalls
  - middleboxes, operating inside network

### 3 architectural principles of the internet

- simple connectivity
- ip protocol
- intelligence & complexity at network edge

### e2e argument

- some network functionality (e.g. reliable data transfer & congestion) can be implemented in network or at network edge

### where's the intelligence?

- 20th c. phone net: intelligence & computing at network switches
- internet (pre 2005): intelligence & computing at edge
- internet (post 2005): programmable network devices, intelligence, computing, & massive app level infrastructure at edge
