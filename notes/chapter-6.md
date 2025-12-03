# chapter 6 - link layer

### toc

- intro
- error detection & correction
- lans
  - addressing, arp
  - ethernet
  - switches
  - vlans
- link virtualization: mpls
- data center networking

## intro

### intro

- terminology
  - hosts, routers: nodes
  - comm channels that connect adjacent nodes along comm path: links
    - wired or wireless
    - lans
  - layer 2 pkt: frame, encapsulates datagram
- link layer has responsibility of transfering datagram from one node to physically adjacent node over link

### context

- datagram transferred by different link protocols over different links
  - wifi, ethernet, etc
- each link protocol provides different services
  - may or may not provide reliable data transfer over link

### transport analogy

- trip from princeton to lausanne
  - car: princeton to jfk
  - plane: jfk to geneva
  - train: geneva to lausanne
- tourist is a datagram
- transport segment is comm link
- transport mode is link layer protocol
- travel agent is routing algorithm

### link layer services

- framing & link access
  - encapsulate datagram into frame, adding header & trailer
  - channel access if shared medium
  - mac addrs in frame headers identify src & dst (different from ip addr)
- reliable delivery between adjacent nodes
  - we already know how to do this
  - seldom used on low bit error links
  - wireless links: high error rates
    - why both link level & e2e reliability?
- flow control
  - pacing between adjacent sending & receiving nodes
- error detection
  - errors caused by signal attenuation & noise
  - receiver detects errors, signals retransmission, or drops frame
- error correction
  - receiver identifies & corrects bit errors without retransmission
- half duplex & full duplex
  - with half duplex, nodes at both ends of link can transmit, but not at same time

### host link layer implementation

- in each & every host
- link layer implemented on chip or in nic
- attaches into host's system buses
- combo of hardware, software, & firmware

### interfaces comms

- sending side
  - encapsulates datagram in frame
  - adds error checking bits, rdt, flow control, etc
- receiving side
  - looks for errors, rdt, flow control, etc
  - extracts datagram, passes to upper layer at receiving side

## error detection & correction

### edc (error detection & correction)

- not 100% reliable
  - protocol may miss some errors, but rarely
  - larger edc field yields better detection & correction

### parity checking

- can detect & correct errors without retransmission
  - 2 dimensional parity: detect & correct single bit errors
- single bit parity
  - detect single bit errors
- at receiver
  - compute parity of d received bits
  - compare with received parity bit

### cyclic redundancy check (crc)

- more powerful error detection coding
- d: data bits (given)
- g: bit pattern (generator) of r + 1 bits (given)
- <d, r> = d \* 2^r xor r
- sender: compute r crc bits, r, such that <d, r> exactly divisible by g (mod 2)
  - receiver knows g, divides <d, r> by g. if nonzero remainder, error detected
  - can detect all burst errors less than r + 1 bits
  - widely used in practice (ethernet, 802.11 wifi)

## multiple access protocols

### multiple access links & protocols

- 2 types of links
  - p2p
    - p2p link between ethernet switch & host
    - ppp for dial up internet
  - broadcast (shared wire or medium)
    - old school ethernet
    - upstream hfc in cable based access network
    - 802.11 wireless lan, 4g/5g, satellite

### multiple access protocols

- single shared broadcast protocol
- 2+ simultaneous transmissions by nodes: interference
  - collision if node receives 2+ signals at same time
- multiple access protocol
  - distributed algorithm that determines how nodes can share channel, i.e. determine when node can transmit
  - comm about channel sharing must use channel itself
    - no out of band channel for coordination

### ideal multiple access protocol

- given: multiple access channel of rate r bps
- desiderata
  - when one node wants to transmit, it can send at rate r
  - when m nodes want to transmit, each can send at avg rate r/m
  - fully decentralized
    - no special node to coordinate transmissions
    - no synchronization of clocks or slots
  - simple

### multiple access channel protocols: taxonomy

- channel partitioning
  - divide channel into smaller pieces (time slots, frequency, code)
  - allocate piece to node for exclusive use
- random access
  - channel not divided, allow collisions
  - recover from collisions
- taking turns
  - nodes take turns, but nodes with more to send can take longer turns

### tdma: time division multiple access

- access to channel in rounds
- each station gets fixed length slot (length = pkt transmission time) in each round
- unused slots go idle
- example: 6 station lan, 1, 3, 4 have pkts to send, slots 2, 5, 6 idle

### fdma: frequency division multiple access

- channel spectrum divided into frequency bands
- each station gets fixed frequency band
- unused transmission time in frequency bands go idle
- example: 6 station lan, 1, 3, 4 have pkts to send, frequency bands 2, 5, 6 idle

### random access protocols

- when node has pkt to send
  - transmit at full channel data rate r
  - no a priori coordination among nodes
- 2+ transmitting nodes: collision
- random access protocol specifies how to detect & recover from collisions
- examples
  - aloha, slotted aloha
  - csma, csma/cd, csma/ca

### slotted aloha

- assumptions
  - all frames same size
  - time divided into equal size slots (time to transmit 1 frame)
  - nodes start to transmit only slot beginning
  - nodes are synchronized
  - if 2+ nodes transmit in slot, all nodes detect collision
- operation
  - when node obtains fresh frame, transmits in next slot
    - if no collision, node can send new frame in next slot
    - if collision, node retransmits frame in each subsequent fslot with probability p until success
      - why random?
- pros
  - single active node can continuously transmit at full rate of channel
  - highly decentralized: only slots in nodes need to be in sync
  - simple
- cons
  - collisions, wasting slots
  - idle slots
  - nodes may be able to detect collision in less than time to transmit pkt
  - clock synchronization
- efficiency
  - efficiency: long run fraction of successful slots (many nodes, all with many frames to send)
    - suppose n nodes with many frames to send, each transmits in slot with probability p
      - prob that given node has success in a slot: p(1 - p)^(n - 1)
      - prob that any node has success: np(1 - p)^(n - 1)
      - max efficiency: find p\* that maximizes np(1 - p)^(n - 1)
      - for many nodes, take limit of np(1 - p)^(n - 1) as n goes to infinity, gives 1/e = 0.37
  - at best: used for useful transmissions 37% of the time

### pure aloha

- unslotted aloha: simpler, no synchronization
  - when frame first arrives, transmit immediately
- collision probability increases with no synchronization
  - frame sent at t0 collides with other frames send tin [t0 - 1, t0 + 1]
- pure aloha efficiency: 18%
  - max efficiency: find p\* that maximizes np(1 - p)^(2(n - 1))

### csma (carrier sense multiple access)

- simple csma: listen before transmit
  - if channel sensed idle, transmit entire frame
  - if channel sensed busy, defer
- no interruption
- csma/cd: csma with collision detection
  - collisions detected within short time
  - colliding transmissions aborted, reducing channel wastage
  - collision detection easy with wired, difficult with wireless

### csma collisions

- collisions can still occur with carrier sensing
  - propagation delay means 2 nodes may not hear each other's transmission that just started
- collision: entire pkt transmission time wasted
  - distance & propagation delay play role in determining collision probability

### csma/cd

- reduces amount of time wasted in collisions
  - transmission aborted on collision detection
- efficiency
  - tprop: max prop delay between 2 lan nodes
  - ttrans: time to transmit max size frame
  - goes to 1 as tprop goes to 0 and as ttrans goes to infinity
  - better than aloha, and simple, clean, cheap, and decentralized

### ethernet csma/cd algorithm

- ethernet receives datagram from network layer, creates frame
- if ethernet senses channel
  - if idle, start transmitting
  - if busy, wait until idle
- if entire frame transmitted without collision, done
- after aborting, enter binary (exponential) backoff
  - after mth collision, chooses k at random from {0, 1, 2, ..., 2^n - 1}
  - ethernet waits k \* 512 bit times, returns to step 2
  - more collisions -> longer backoff interval

### taking turns protocols

- channel partitioning protocols
  - share channel efficiently & fairly at high load
  - inefficient at low load: delay in channel access, 1/n bandwidth allocated even if only 1 active node
- random access protocols
  - efficient at low load: single node can fully utilize channel
  - high load: collision overhead
- taking turns protocols
  - look for both of best worlds

### taking turns multiple access channel protocols

- token passing
  - control token msg explicitly passed from one node to next sequentially
    - transmit while holding token
  - concerns
    - token overhead
    - latency
    - token is single point of failure

### cable access network: fdm, tdm, & random access

- multiple downstream (broadcast) fdm channels: up to 1.6 Gbps/channel
  - single cmts transmits into channels
- multiple upstream channels (up to 1 Gbps/channel)
  - multiple access: all users contend (random access) for certain upstream channel time slots; others assigned tdm

### cable access network

- docsis (data over cable service interface spec)
  - fdm over upstream, downstream frequency channels
  - tdm upstream: some slots assigned, some have contention
    - downstream map frame: assigns upstream risks
    - request for upstream slots (& data) transmitted random access (binary backoff) in selected slots

### summary of mac protocols

- channel partitioning by time, frequency, or code
  - time division, frequency division
- random access (dynamic)
  - aloha, s-aloha, csma, csma/cd
  - carrier sensing: easy in some media (wire), hard in others (wireless)
  - csma/cd used in ethernet
  - csma/ca used in 802.11
- taking turns
  - polling from central site, token passing
  - bluetooth, fddi, token ring

## lans

## addressing & arp

### mac addrs

- 32 bit ip addr
  - network layer addr for interface
  - used for layer 3 forwarding
- mac (or lan or physical or ethernet) addr
  - function: used locally to get frame from one interface to another interface in same subnet
  - 48 bit mac addr (for most lans) burned in nic rom, also sometimes software settable
- mac addr allocation administered by ieee
- manufacturer buys portion of mac addr space to assure uniqueness
- analogy
  - mac addr: like social security number
  - ip addr: like postal addr
- mac flat addr: portability
  - can move interface from one lan to another
  - recall ip addr not portable: depends on ip subnet to which node it is attached

### arp (addr resolution protocol)

- arp table: each ip node (host, router) on lan has table
  - ip/mac addr mappings for some lan nodes
    - <ip addr, mac addr, ttl>
  - ttl (time to live): time after which addr mapping will be forgotten (typically 20 min)

### arp in action

- example: a wants to send datagram to b
- a broadcasts arp query, containing b's ip addr
  - all nodes on lan receive arp query
- when b receives a's arp msg, adds a to its arp table, sends frame back to a

### routing through another subnet: addressing

- scenario: a and b on different subnets but both connected to r
- walkthrough sending a datagram from a to b via r
  - focus on addressing - at ip (datagram) & mac (frame) layer levels
  - assume that
    - a knows b's ip
    - a knows ip addr of first hop router
    - a knows r's mac addr
  - a creates ip datagram with ip (src a, dst b)
  - a creates link layer frame containing ip datagram from a to b
    - r's mac addr is frame's dst
  - frame sent from a to r
  - frame received at r, datagram removed, passed up to ip
  - r determines outgoing interface, passes datagram with ip src a, dst b to link layer
  - r creates link layer frame containing datagram from a to b. frame dst addr: b's mac addr
  - r determines outgoing interface, passes datagram with ip src a, dst b to link layer
  - r creates link layer frame containing a to b ip datagram. frame dst addr: b's mac addr
  - transmits link layer frame

## ethernet

### ethernet

- dominant wired lan medium
  - first widely used lan tech
  - simple, cheap
  - kept up with speed race: 10 Mbps-400 Gbps
  - single chip, multiple speeds
- physical topology
  - bus: popular through mid 90s
    - all nodes in same collision domain (can collide with each other)
  - switched: prevails today
    - active link layer 2 switch in center
    - each spoke runs a separate ethernet protocol (nodes do not collide with each other)
- frame structure
  - sending interface encapsulates ip datagram (or other network layer protocol pkt) in ethernet frame
  - preamble
    - used to synchronize receiver & sender clock rates
    - 7 bytes of 10101010 followed by one byte of 10101011
  - addrs: 6 byte src & dst mac addrs
    - if adapter receives frame with matching dst addr or with broadcast addr (e.g. arp pkt), passes data in frame to network layer protocol
      - otherwise, discard frame
  - type: indicates higher layer protocol
    - mostly ip but others possible, e.g. novell ipx, appletalk
    - used to demux at receiver
  - crc at receiver
    - error detected: frame dropped

### ethernet: unreliable, connectionless

- connectionless: no handshaking between sender & receiver
- unreliable: receiver doesn't send ack or nak to sender
  - data in dropped frames recovered only if initial sender uses higher layer rdt (e.g. tcp), otherwise dropped data lost
- ethernet's multiple access protocol: unslotted csma/cd with binary backoff

### 802.3 ethernet standards: link & physical layers

- many different ethernet standards
  - common multiple access protocol & frame format
  - different speeds: 2 Mbps, ..., 100 Mpbs, 1 Gbps, 10 Gbps, 40 Gbps, 80 Gbps
    - different physical media: fiber, cable

## switches

### switches

- link layer device taking an active role
  - store & forward ethernet (or other type of) frames
  - examine incoming frame's mac addr, selectively forward frame to >= 1 outgoing links when frame is to be forwarded on segment, uses csma/cd to access segment
- transparent: hosts unaware of presence of switches
- plug & play, self learning
  - switches do not need to be configured

### multiple simultaneous transmissions

- hosts have dedicated & direct connection to switch
- switches buffer pkts
- ethernet protocol used on each incoming link
  - no collisions, full duplex
  - each link is its own collision domain
- switching: a to a' and b to b' can transmit simultaneously without collisions
  - but a to a' and c to a' cannot happen simultaneously

### switch forwarding table

- how does a switch know a' reachable via interface 4 and b' reachable via interface 5?
  - each switch has a switch table
    - each entry: (host mac addr, interface to reach host, time stamp)
    - looks like a routing table
- how are entries created & maintained in switch table?
  - something like a routing protocol

### self learning

- switch learns which hosts can be reached through which interfaces
  - when frame received, switch learns location of sender: incoming lan segment
  - records (sender, location) in table

### frame filtering & forwarding

- when frame received at switch
  1. record incoming link & mac addr of sending host
  2. index switch table using dst mac addr
  3. if entry found for dst
  - if dst on segment from which frame arrived, then drop frame, else forward frame on interface indicated by entry
  - else flood

### interconnecting switches

- self learning switches can be connected together
- sending from a to g - how does s1 know to forward frame dst to g via s4 and s3?
  - self learning (flood, then find switch from where response came)

### umass campus network - detail

- 4 firewalls
- 10 routers
- 2000+ network switches
- 6000 wireless access points
- 3000 active wired network jacks
- 55000 active end user wireless devices
  - all built, operated, maintained by ~15 people

### switches vs routers

- both are store & forward
  - routers: network layer devices (examine network layer headers)
  - switches: link layer devices (examine link layer headers)
- both have forwarding tables
  - routers: compute tables using routing algorithms & ip addrs
  - switches: learn forwarding table using flooding, learning, & mac addrs

## vlans

### vlan motivation

- what happens as lan sizes scale & users change point of attachment?
  - single broadcast domain
    - scaling: all layer 2 broadcast traffic (arp, dhcp, unknown mac) must cross entire lan
    - efficiency, security, privacy issues
  - administrative issues
    - cs user moves office to ee - physically attached to ee switch, but wants to remain logically attached to cs switch

### port based vlans

- vlan
  - switch(es) supporting vlan capabilities can be configured to define multiple virtual lans over single physical lan infrastructure
- port based vlan
  - switch ports grouped (by switch mgmt software) so that single physical switch operates as multiple virtual switches
- traffic isolation - frames to/from ports 1-8 can only reach ports 1-8
  - can also define vlan based on mac addrs of endpoints, rather than switch port
- dynamic membership: ports can be dynamically assigned among vlans
- forwarding between vlans: done via routing (just as with separate switches)
  - in practice, vendors sell combined switches + routers

### vlans spanning multiple switches

- trunk port: carries frames between vlans defined over multiple physical switches
  - frames forwarded within vlan between switches can't be vanilla 802.1 frames (must carry vlan id info)
  - 802.1q protocol adds/removes additional header fields for frames forwarded between trunk ports

### 802.1q vlan frame format

- after src addr but before type:
  - 2 byte tag protocol identifier (value 81-00)
  - tag control information (12 bit vlan id field, 3 bit priority field like ip tos)
- recompute crc

### evpn: ethernet vpns (aka vxlans)

- layer 2 ethernet switches logically connected to each other (e.g. using ip as an underlay)
  - ethernet frames carried within ip datagrams between sites
  - tunneling scheme to overlay layer 2 networks on top of layer 3 networks runs over existing networking infrastructure & provides a means to stretch a layer 2 network

## link virtualization: mpls

### multiprotocol label switching (mpls)

- goal: high speed ip forwarding among network of mpls capable routers, using fixed length label instead of shortest prefix matching
  - faster lookup using fixed length id
  - borrowing ideas from virtual circuit approach
  - ip datagram still keeps ip addr

### mpls capable routers

- aka label switched router
- forward pkts to outgoing interface based only on label value (don't inspect ip addr)
  - mpls forwarding table distinct from ip forwarding tables
- flexibility: mpls forwarding decisions can differ from those of ip
  - use dst & src addrs to route flows to same dst differently (traffic engineering)
  - reroute flows quickly if link fails: precomputed backup paths

### mpls vs ip paths

- ip routing: path to dst determined by dst addr alone
- mpls routing: path to dst can be based on src & dst addr
  - flavor of generalized forwarding
  - fast reroute: precompute backup routes in case of link failure

### mpls signaling

- modify ospf & is-is link state flooding protocols to carry info used by mpls routing
  - e.g. link bandwidth, amount of reserved link bandwidth
- entry mpls router uses rsvp-te signaling protocol to set up mpls forwarding at downstream routers

## data center networking

### datacenter networks

- 10s to 100s of thousands of hosts, often closely coupled, in close proximity
  - ebusiness
  - content servers
  - search engines, data mining
- challenges
  - multiple apps, each serving massive numbers of clients
  - reliability
  - managing/balancing load, avoiding processing, networking, & data bottlenecks

### datacenter network elements

- border routers
  - connections outside datacenter
- tier 1 (core) switches
  - connecting to ~16 t2s below
- tier 2 (aggregation switches)
  - connecting to ~16 tors below
- top of rack (tor) (access) switches
  - one per rack, 100G-400G ethernet to blades
- server racks
  - 20-40 server blades: hosts

### datacenter networks: multipath

- rich interconnection among switches & racks
  - increased throughput between racks (multiple routing paths possible)
  - increased reliability via redundancy

### datacenter networks: app layer routing

- load balancer: app layer routing
  - receives external client requests
  - directs workload within datacenter
  - returns results to external client, hiding datacenter internals from client

### datacenter networks: protocol innovations

- link layer
  - roce: remote dma (rdma) over converged ethernet
- transport layer
  - ecn (explicit congestion notification) used in transport layer congestion protocol (dctcp, tdqcn)
  - experimentation with hop by hop (backpressure) congestion control
- routing, mgmt
  - sdn widely used within/among orgs' datacenters
  - place related services, data as close as possible (e.g. in same rack or nearby rack) to minimize tier 2 & tier 1 comms

### orion: google's new sdn control plane for internal datacenter (jupiter) & wan (b4)

- routing (intradomain, ibgp), traffic engineering: implemented in apps on top of orion core
- edge-edge flow based controls (e.g. coflow scheduling) to meet contract slas
- mgmt: pub-sub distributed microservices in orion core, openflow for switch signaling/monitoring
- no routing protocols, congestion control partially also managed by sdn rather than by protocol
- potential harbinger of death of protocols

## day in the life of a web request

### scenario

- arriving mobile client attaches to network & requests web page
- connection phase
  - connecting laptop needs to get its own ip addr, addr of first hop router, & addr of dns server: use dhcp
  - dhcp request encapsulated in udp, encapsulated in ip, encapsulated in 802.3 ethernet
  - ethernet frame broadcast on lan, received at router running dhcp server
  - ethernet demuxed to ip demuxed, udp demuxed to dhcp
  - dhcp server formulates dhcp ack containing client's ip addr, ip addr of first hop router for client, name & ip of dns server
  - encapsulation at dhcp server, frame forwarded (switch learning) through lan, demuxing at client
  - dhcp client receives dhcp ack
- arp (before dns, before http)
  - before sending http request, need ip addr of google.com: dns
  - dns query created, encapsulated in udp, encapsulated in ip, encapsulated in ethernet. to send frame to router, need mac addr of router interface: arp
  - arp query broadcast, received by router, which replies with arp reply giving mac addr of router interface
  - client now knows mac addr of first hop router, so now can send frame containing dns query
- using dns
  - ip datagram containing dns query forwarded via lan switch from client to first hop router
  - ip datagram forwarded from campus network into isp network, routed (tables created by rip, ospf, is-is, and/or bgp) to dns server
  - demuxed to dns
  - dns replies to client with ip addr of google.com
- tcp connection carrying http
  - to send http request, client first opens tcp socket to web server
  - tcp syn segment interdomain routed to web
  - server responds with synack
  - client sends ack -> connection established
- http request/reply
  - http request sent into tcp socket
  - ip datagram containing http request routed to google
  - web server responds to with http reply containing web page
  - ip datagram containing http reply routed back to client
